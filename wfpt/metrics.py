"""Performance metrics for the WFPT test statistic and reporting."""

from __future__ import annotations

import numpy as np
import pandas as pd


def sharpe_annualized(returns: pd.Series | np.ndarray, periods_per_year: int = 252) -> float:
    r = np.asarray(returns, dtype=float)
    r = r[~np.isnan(r)]
    if r.size < 2 or r.std(ddof=1) == 0.0:
        return 0.0
    return float(np.sqrt(periods_per_year) * r.mean() / r.std(ddof=1))


def profit_factor(returns: pd.Series | np.ndarray) -> float:
    r = np.asarray(returns, dtype=float)
    gains = r[r > 0].sum()
    losses = -r[r < 0].sum()
    if losses == 0.0:
        return float("inf") if gains > 0 else 0.0
    return float(gains / losses)


def cagr(returns: pd.Series | np.ndarray, periods_per_year: int = 252) -> float:
    r = np.asarray(returns, dtype=float)
    if r.size == 0:
        return 0.0
    total_log = r.sum()
    years = r.size / periods_per_year
    if years <= 0:
        return 0.0
    return float(np.exp(total_log / years) - 1.0)
