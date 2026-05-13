"""Sanity tests for the wfpt package — fast, deterministic, runnable standalone.

Run: conda run -n rappi python tests/sanity.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

from wfpt.data import make_features
from wfpt.permutation import permute_bars
from wfpt.metrics import sharpe_annualized
from wfpt.walkforward import walkforward_oos
from wfpt.mcpt import run_wfpt


def synthetic_ohlc(n: int = 1500, seed: int = 0) -> pd.DataFrame:
    """White-noise log-returns -> synthetic OHLC with no signal."""
    rng = np.random.default_rng(seed)
    log_ret = rng.normal(0.0, 0.012, size=n)
    close = 100.0 * np.exp(np.cumsum(log_ret))
    open_ = close * np.exp(rng.normal(0, 0.002, n))
    high = np.maximum(open_, close) * np.exp(np.abs(rng.normal(0, 0.003, n)))
    low = np.minimum(open_, close) * np.exp(-np.abs(rng.normal(0, 0.003, n)))
    idx = pd.date_range("2010-01-01", periods=n, freq="B")
    return pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close,
         "Volume": np.ones(n)},
        index=idx,
    )


def test_permutation_preserves_distribution() -> None:
    df = synthetic_ohlc(1000)
    start = 200
    p1 = permute_bars(df, start_idx=start, seed=0)
    p2 = permute_bars(df, start_idx=start, seed=1)

    pre = ["Open", "High", "Low", "Close"]
    np.testing.assert_allclose(
        p1[pre].iloc[:start].to_numpy(),
        df[pre].iloc[:start].to_numpy(),
        rtol=1e-12, atol=1e-12,
        err_msg="train segment changed",
    )

    real_ret = np.log(df["Close"]).diff().iloc[start:].dropna()
    perm_ret = np.log(p1["Close"]).diff().iloc[start:].dropna()
    assert abs(real_ret.mean() - perm_ret.mean()) < 5e-3, "mean drift too large"
    assert abs(real_ret.std() - perm_ret.std()) < 5e-3, "std drift too large"

    assert not p1["Close"].iloc[start:].equals(p2["Close"].iloc[start:]), \
        "different seeds produced same path"

    assert (p1["High"] >= p1[["Open", "Close"]].max(axis=1)).all()
    assert (p1["Low"] <= p1[["Open", "Close"]].min(axis=1)).all()
    print("[ok] permutation: train preserved, marginals close, OHLC consistent")


def test_walkforward_lengths() -> None:
    df = synthetic_ohlc(1200)
    X, y, r = make_features(df)
    train_window = 500
    step = 21
    oos = walkforward_oos(X, y, r, train_window=train_window, step=step)
    expected = len(X) - train_window
    assert len(oos) == expected, f"expected {expected} OOS rows, got {len(oos)}"
    assert oos.index.is_monotonic_increasing
    print(f"[ok] walkforward: produced {len(oos)} OOS rows as expected")


def test_parallel_determinism_and_null() -> None:
    df = synthetic_ohlc(900)
    res_seq = run_wfpt(
        df,
        n_permutations=8,
        train_window=400,
        step=42,
        n_jobs=1,
        master_seed=123,
        progress=False,
    )
    res_par = run_wfpt(
        df,
        n_permutations=8,
        train_window=400,
        step=42,
        n_jobs=2,
        master_seed=123,
        progress=False,
    )
    np.testing.assert_allclose(res_seq.perm_sharpes, res_par.perm_sharpes, atol=1e-10)
    assert res_seq.real_sharpe == res_par.real_sharpe
    assert 0.0 < res_seq.p_value <= 1.0
    print(
        f"[ok] mcpt: deterministic across n_jobs; "
        f"real_sharpe={res_seq.real_sharpe:+.3f}, p_value={res_seq.p_value:.3f} "
        f"(synthetic null, expected ~0.5 ± noise)"
    )


def main() -> None:
    test_permutation_preserves_distribution()
    test_walkforward_lengths()
    test_parallel_determinism_and_null()
    print("\nAll sanity tests passed.")


if __name__ == "__main__":
    main()
