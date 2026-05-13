"""Data loading and feature engineering for the S&P 500 WFPT pipeline."""

from __future__ import annotations

import numpy as np
import pandas as pd
import yfinance as yf


def load_sp500(start: str = "2005-01-01", end: str = "2024-12-31") -> pd.DataFrame:
    """Download S&P 500 OHLCV daily bars from Yahoo Finance.

    Returns a DataFrame indexed by date with columns Open, High, Low, Close, Volume.
    """
    df = yf.download(
        "^GSPC",
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
    )
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna().copy()
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"
    return df


def _rsi(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / window, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    rsi = 100.0 - 100.0 / (1.0 + rs)
    return rsi.fillna(50.0)


def make_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Build feature matrix X, target y, and forward returns r used for PnL.

    - X: lagged log-returns (1..5), rolling vol (5, 21), RSI(14), MA-ratio (5/21).
    - y: sign of next-day log-return in {-1, +1}.
    - r: next-day log-return aligned to X (so PnL = signal_t * r_t).
    """
    close = df["Close"].astype(float)
    log_ret = np.log(close).diff()

    feats = pd.DataFrame(index=df.index)
    for k in range(1, 6):
        feats[f"ret_lag_{k}"] = log_ret.shift(k)
    feats["vol_5"] = log_ret.rolling(5).std()
    feats["vol_21"] = log_ret.rolling(21).std()
    feats["rsi_14"] = _rsi(close, 14)
    ma5 = close.rolling(5).mean()
    ma21 = close.rolling(21).mean()
    feats["ma_ratio"] = (ma5 / ma21) - 1.0

    fwd_ret = log_ret.shift(-1)
    y = np.sign(fwd_ret).replace(0.0, 1.0)

    valid = feats.dropna().index.intersection(fwd_ret.dropna().index)
    X = feats.loc[valid]
    y = y.loc[valid].astype(int)
    r = fwd_ret.loc[valid]
    return X, y, r
