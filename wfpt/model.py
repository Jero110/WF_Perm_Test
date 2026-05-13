"""XGBoost classifier wrapper for the WFPT pipeline.

Hyperparameters are intentionally fixed: the WFPT measures whether the *model
specification* (features + algorithm + parameters) extracts genuine signal,
not whether we can find a lucky combo. Tuning per-permutation would inflate
type-I error.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from xgboost import XGBClassifier


def default_xgb_params() -> dict:
    return dict(
        n_estimators=120,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        tree_method="hist",
        objective="binary:logistic",
        eval_metric="logloss",
        n_jobs=1,
        verbosity=0,
        random_state=0,
    )


def fit_xgb(X: pd.DataFrame, y: pd.Series, params: dict | None = None) -> XGBClassifier:
    params = {**default_xgb_params(), **(params or {})}
    y_bin = (y > 0).astype(int).to_numpy()
    model = XGBClassifier(**params)
    model.fit(X.to_numpy(), y_bin)
    return model


def predict_signal(model: XGBClassifier, X: pd.DataFrame) -> pd.Series:
    """Return position signal in {-1, +1} indexed like X."""
    proba = model.predict_proba(X.to_numpy())[:, 1]
    sig = np.where(proba >= 0.5, 1, -1)
    return pd.Series(sig, index=X.index, name="signal")
