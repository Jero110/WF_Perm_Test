"""Bar permutation à la Aronson (Evidence-Based Technical Analysis, 2007).

Decomposes each OHLC bar into four independent log-space components:

    gap_t  = log(O_t)            - log(C_{t-1})            # overnight
    body_t = log(C_t)            - log(O_t)                # intraday body
    high_t = log(H_t)            - log(max(O_t, C_t))      # upper wick (>= 0)
    low_t  = log(min(O_t, C_t))  - log(L_t)                # lower wick  (>= 0)

The components from `start_idx` onward are permuted independently with the same
RNG, then OHLC is reconstructed from the last unpermuted Close. The pre-train
segment (0..start_idx) is left intact so the model still trains on real data;
only the out-of-sample window has its predictive structure destroyed.

This preserves the marginal distribution of bar shapes while breaking
serial dependence — exactly the null hypothesis for the WFPT.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _decompose(df: pd.DataFrame) -> dict[str, np.ndarray]:
    o = np.log(df["Open"].to_numpy(dtype=float))
    h = np.log(df["High"].to_numpy(dtype=float))
    l = np.log(df["Low"].to_numpy(dtype=float))
    c = np.log(df["Close"].to_numpy(dtype=float))

    gap = np.empty_like(o)
    gap[0] = 0.0
    gap[1:] = o[1:] - c[:-1]

    body = c - o
    high = h - np.maximum(o, c)
    low = np.minimum(o, c) - l
    return {"gap": gap, "body": body, "high": high, "low": low, "log_c0": c[0]}


def permute_bars(
    df: pd.DataFrame,
    start_idx: int,
    seed: int | np.random.SeedSequence,
) -> pd.DataFrame:
    """Return a new OHLC DataFrame with bars permuted from `start_idx` onward.

    The first `start_idx` rows are returned unchanged. From `start_idx` onward,
    the (gap, body, high, low) components are independently permuted and the
    OHLC reconstructed continuing from the last untouched Close.

    Parameters
    ----------
    df : DataFrame with columns Open, High, Low, Close (Volume optional).
    start_idx : int, first index to permute. Must satisfy 1 <= start_idx < len(df).
    seed : int or SeedSequence for the RNG.
    """
    n = len(df)
    if not (1 <= start_idx < n):
        raise ValueError(f"start_idx must be in [1, {n}), got {start_idx}")

    rng = np.random.default_rng(seed)
    comps = _decompose(df)

    perm_len = n - start_idx
    perms = {
        name: rng.permutation(perm_len)
        for name in ("gap", "body", "high", "low")
    }

    log_o = np.log(df["Open"].to_numpy(dtype=float)).copy()
    log_h = np.log(df["High"].to_numpy(dtype=float)).copy()
    log_l = np.log(df["Low"].to_numpy(dtype=float)).copy()
    log_c = np.log(df["Close"].to_numpy(dtype=float)).copy()

    gap_oos = comps["gap"][start_idx:][perms["gap"]]
    body_oos = comps["body"][start_idx:][perms["body"]]
    high_oos = comps["high"][start_idx:][perms["high"]]
    low_oos = comps["low"][start_idx:][perms["low"]]

    prev_close = log_c[start_idx - 1]
    for i in range(perm_len):
        idx = start_idx + i
        log_o[idx] = prev_close + gap_oos[i]
        log_c[idx] = log_o[idx] + body_oos[i]
        top = max(log_o[idx], log_c[idx])
        bot = min(log_o[idx], log_c[idx])
        log_h[idx] = top + high_oos[i]
        log_l[idx] = bot - low_oos[i]
        prev_close = log_c[idx]

    out = df.copy()
    out["Open"] = np.exp(log_o)
    out["High"] = np.exp(log_h)
    out["Low"] = np.exp(log_l)
    out["Close"] = np.exp(log_c)
    return out
