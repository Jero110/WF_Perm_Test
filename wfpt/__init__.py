"""Walk-Forward Permutation Test (à la Aronson) — paralelizado."""

from wfpt.data import load_sp500, make_features
from wfpt.permutation import permute_bars
from wfpt.model import fit_xgb, predict_signal, default_xgb_params
from wfpt.walkforward import walkforward_oos
from wfpt.metrics import sharpe_annualized, profit_factor, cagr
from wfpt.mcpt import run_wfpt
from wfpt import plotting

__all__ = [
    "load_sp500",
    "make_features",
    "permute_bars",
    "fit_xgb",
    "predict_signal",
    "default_xgb_params",
    "walkforward_oos",
    "sharpe_annualized",
    "profit_factor",
    "cagr",
    "run_wfpt",
    "plotting",
]
