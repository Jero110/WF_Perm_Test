"""Monte Carlo Walk-Forward Permutation Test orchestrator (parallel).

For each permutation:
    1. Permute OHLC bars from the train boundary onward (Aronson).
    2. Recompute features on the permuted prices.
    3. Run the full anchored walk-forward.
    4. Compute the test statistic (Sharpe) on OOS returns.

The real (unpermuted) WF is run once, then `n_permutations` permuted WFs are
dispatched across joblib workers. Each worker receives an independent seed
spawned from the master `SeedSequence` so results are reproducible regardless
of `n_jobs`.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from time import perf_counter

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm.auto import tqdm

from wfpt.data import make_features
from wfpt.metrics import sharpe_annualized
from wfpt.permutation import permute_bars
from wfpt.walkforward import walkforward_oos


@dataclass
class WFPTResult:
    real_sharpe: float
    perm_sharpes: np.ndarray
    p_value: float
    real_oos_returns: pd.Series
    perm_oos_returns: list[pd.Series]
    elapsed_seconds: float
    config: dict = field(default_factory=dict)

    def summary(self) -> pd.DataFrame:
        perm = self.perm_sharpes
        return pd.DataFrame(
            {
                "value": [
                    self.real_sharpe,
                    perm.mean(),
                    perm.std(ddof=1),
                    np.quantile(perm, 0.05),
                    np.quantile(perm, 0.95),
                    int((perm >= self.real_sharpe).sum()),
                    self.p_value,
                    self.elapsed_seconds,
                ]
            },
            index=[
                "real_sharpe",
                "null_mean",
                "null_std",
                "null_q05",
                "null_q95",
                "n_perm_geq_real",
                "p_value",
                "elapsed_seconds",
            ],
        )


@contextlib.contextmanager
def _tqdm_joblib(tqdm_object: tqdm):
    """Bridge joblib progress into a tqdm bar."""
    from joblib.parallel import BatchCompletionCallBack

    class TqdmBatchCompletionCallback(BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old = BatchCompletionCallBack
    BatchCompletionCallBack = TqdmBatchCompletionCallback  # noqa: F841
    import joblib.parallel as _jp

    _jp.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        _jp.BatchCompletionCallBack = old
        tqdm_object.close()


def _one_permutation(
    df_ohlc: pd.DataFrame,
    start_idx: int,
    train_window: int,
    step: int,
    model_params: dict | None,
    seed: int,
) -> tuple[float, pd.Series]:
    df_perm = permute_bars(df_ohlc, start_idx=start_idx, seed=seed)
    X, y, r = make_features(df_perm)
    oos = walkforward_oos(
        X, y, r,
        train_window=train_window,
        step=step,
        model_params=model_params,
    )
    return sharpe_annualized(oos), oos


def run_wfpt(
    df_ohlc: pd.DataFrame,
    n_permutations: int = 1000,
    train_window: int = 252 * 4,
    step: int = 21,
    model_params: dict | None = None,
    n_jobs: int = -1,
    master_seed: int = 42,
    progress: bool = True,
) -> WFPTResult:
    """Run the full Walk-Forward Permutation Test.

    `train_window` is in feature-space rows (after make_features drops NaNs).
    `start_idx` for permutation is computed in OHLC-space rows so that the
    pre-train OHLC bars are kept intact.
    """
    t0 = perf_counter()

    X_real, y_real, r_real = make_features(df_ohlc)
    if train_window >= len(X_real):
        raise ValueError(
            f"train_window {train_window} >= feature rows {len(X_real)}"
        )

    first_oos_date = X_real.index[train_window]
    start_idx = df_ohlc.index.get_loc(first_oos_date)

    real_oos = walkforward_oos(
        X_real, y_real, r_real,
        train_window=train_window,
        step=step,
        model_params=model_params,
    )
    real_sharpe = sharpe_annualized(real_oos)

    ss = np.random.SeedSequence(master_seed)
    child_seeds = [int(s.generate_state(1)[0]) for s in ss.spawn(n_permutations)]

    iterator = tqdm(
        total=n_permutations,
        desc=f"WFPT (n_jobs={n_jobs})",
        disable=not progress,
    )
    with _tqdm_joblib(iterator):
        results = Parallel(n_jobs=n_jobs, backend="loky")(
            delayed(_one_permutation)(
                df_ohlc, start_idx, train_window, step, model_params, seed
            )
            for seed in child_seeds
        )

    perm_sharpes = np.array([s for s, _ in results], dtype=float)
    perm_oos_returns = [oos for _, oos in results]

    p_value = (1.0 + (perm_sharpes >= real_sharpe).sum()) / (1.0 + n_permutations)
    elapsed = perf_counter() - t0

    return WFPTResult(
        real_sharpe=real_sharpe,
        perm_sharpes=perm_sharpes,
        p_value=p_value,
        real_oos_returns=real_oos,
        perm_oos_returns=perm_oos_returns,
        elapsed_seconds=elapsed,
        config=dict(
            n_permutations=n_permutations,
            train_window=train_window,
            step=step,
            n_jobs=n_jobs,
            master_seed=master_seed,
            start_idx=start_idx,
            first_oos_date=str(first_oos_date.date()),
        ),
    )
