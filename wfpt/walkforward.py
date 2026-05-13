"""Anchored walk-forward out-of-sample evaluation.

At each step the model is refit on all data from the start up to time `t`,
then used to predict the next `step` bars. The realized strategy return is
`signal_t * forward_return_t`.

Anchored (vs rolling) means the train window grows over time — closer to how
a hedge-fund desk actually retrains in production.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd

from WF_Perm_Test.wfpt.model import fit_xgb, predict_signal


def walkforward_oos(
    X: pd.DataFrame,
    y: pd.Series,
    fwd_ret: pd.Series,
    train_window: int,
    step: int = 21,
    fit_fn: Callable | None = None,
    predict_fn: Callable | None = None,
    model_params: dict | None = None,
) -> pd.Series:
    """Run anchored walk-forward, return realized OOS strategy log-returns.

    Parameters
    ----------
    X, y, fwd_ret : aligned feature matrix, target, and forward returns.
    train_window : initial train length (also the index of the first OOS bar).
    step : how many bars to predict between refits.
    fit_fn, predict_fn : injected for testing; default uses XGBoost wrappers.
    """
    fit_fn = fit_fn or fit_xgb
    predict_fn = predict_fn or predict_signal

    n = len(X)
    if train_window >= n:
        raise ValueError(f"train_window {train_window} >= data length {n}")

    pieces: list[pd.Series] = []
    for t in range(train_window, n, step):
        end = min(t + step, n)
        X_tr, y_tr = X.iloc[:t], y.iloc[:t]
        X_te = X.iloc[t:end]
        model = fit_fn(X_tr, y_tr, model_params)
        sig = predict_fn(model, X_te)
        pnl = sig.astype(float) * fwd_ret.iloc[t:end].astype(float)
        pieces.append(pnl)

    return pd.concat(pieces).rename("oos_return")
