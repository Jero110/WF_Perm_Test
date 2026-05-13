"""Plotting utilities — minimal academic style (light, serif).

Designed to render cleanly in PDF/print: white background, serif fonts,
muted palette, no chart junk.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle


PALETTE = {
    "ink":      "#1B1F23",
    "real":     "#B5341B",  # terracotta — the strategy
    "null":     "#2E4A6B",  # navy        — the permutations
    "muted":    "#8A8F94",
    "band":     "#C9D3E0",
    "rule":     "#D6D2C7",
    "paper":    "#FBFAF7",
}


def use_academic_style() -> None:
    """Apply a minimal academic matplotlib style (idempotent)."""
    mpl.rcParams.update({
        "figure.facecolor":  PALETTE["paper"],
        "axes.facecolor":    PALETTE["paper"],
        "savefig.facecolor": PALETTE["paper"],
        "font.family":       "serif",
        "font.serif":        ["Computer Modern Roman", "DejaVu Serif", "Times New Roman"],
        "mathtext.fontset":  "cm",
        "font.size":         11,
        "axes.titlesize":    13,
        "axes.titleweight":  "regular",
        "axes.labelsize":    11,
        "axes.edgecolor":    PALETTE["ink"],
        "axes.linewidth":    0.8,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.grid":         True,
        "grid.color":        PALETTE["rule"],
        "grid.linewidth":    0.5,
        "grid.alpha":        0.8,
        "xtick.color":       PALETTE["ink"],
        "ytick.color":       PALETTE["ink"],
        "xtick.direction":   "out",
        "ytick.direction":   "out",
        "legend.frameon":    False,
        "legend.fontsize":   10,
        "figure.dpi":        110,
        "savefig.dpi":       200,
    })


def plot_null_distribution(
    real_value: float,
    perm_values: np.ndarray,
    p_value: float,
    metric_name: str = "Sharpe ratio (annualized)",
    bins: int = 40,
    ax: plt.Axes | None = None,
):
    use_academic_style()
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 4.2))

    ax.hist(
        perm_values, bins=bins,
        color=PALETTE["null"], alpha=0.85,
        edgecolor=PALETTE["paper"], linewidth=0.6,
        label="Permutations (null)",
    )
    ax.axvline(
        real_value,
        color=PALETTE["real"], linewidth=1.6,
        label=f"Real strategy = {real_value:.3f}",
    )

    ymax = ax.get_ylim()[1]
    ax.text(
        real_value, ymax * 0.93,
        f"  $p$-value = {p_value:.3f}",
        color=PALETTE["real"], fontsize=11,
        ha="left", va="top",
    )

    ax.set_xlabel(metric_name)
    ax.set_ylabel("Permutation count")
    ax.set_title("Null distribution of the test statistic")
    ax.legend(loc="upper left")
    return ax


def plot_equity_bands(
    real_returns: pd.Series,
    perm_returns: list[pd.Series],
    quantiles: tuple[float, float] = (0.05, 0.95),
    ax: plt.Axes | None = None,
):
    use_academic_style()
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 4.6))

    real_eq = real_returns.cumsum()
    aligned = pd.concat(
        [r.reindex(real_returns.index).cumsum() for r in perm_returns],
        axis=1,
    )
    qlo = aligned.quantile(quantiles[0], axis=1)
    qhi = aligned.quantile(quantiles[1], axis=1)
    median = aligned.quantile(0.5, axis=1)

    ax.fill_between(
        real_eq.index, qlo, qhi,
        color=PALETTE["band"], alpha=0.95,
        label=f"Permutation band [{int(quantiles[0]*100)}, {int(quantiles[1]*100)}]%",
    )
    ax.plot(
        median.index, median,
        color=PALETTE["null"], linewidth=1.0,
        linestyle="--", label="Permutation median",
    )
    ax.plot(
        real_eq.index, real_eq,
        color=PALETTE["real"], linewidth=1.6,
        label="Real strategy",
    )
    ax.axhline(0, color=PALETTE["muted"], linewidth=0.6)

    ax.set_ylabel("Cumulative log-return")
    ax.set_title("Out-of-sample equity curve vs permutation envelope")
    ax.legend(loc="upper left")
    return ax


def plot_walkforward_schema(
    n_total: int = 12,
    train_window: int = 4,
    step: int = 2,
    ax: plt.Axes | None = None,
):
    """Conceptual diagram of anchored walk-forward."""
    use_academic_style()
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 3.6))

    folds = []
    t = train_window
    while t < n_total:
        folds.append((t, min(t + step, n_total)))
        t += step

    height = 0.6
    for i, (t, end) in enumerate(folds):
        y = -i
        ax.add_patch(Rectangle(
            (0, y - height / 2), t, height,
            facecolor=PALETTE["null"], alpha=0.85, edgecolor="none",
        ))
        ax.add_patch(Rectangle(
            (t, y - height / 2), end - t, height,
            facecolor=PALETTE["real"], alpha=0.9, edgecolor="none",
        ))
        ax.text(-0.4, y, f"fold {i+1}", ha="right", va="center", fontsize=10)

    ax.add_patch(Rectangle((0, 1.4), 0.6, 0.4, facecolor=PALETTE["null"]))
    ax.text(0.8, 1.6, "train (anchored)", va="center", fontsize=10)
    ax.add_patch(Rectangle((4.2, 1.4), 0.6, 0.4, facecolor=PALETTE["real"]))
    ax.text(5.0, 1.6, "out-of-sample (predict)", va="center", fontsize=10)

    ax.set_xlim(-2, n_total + 0.5)
    ax.set_ylim(-len(folds) - 0.5, 2.2)
    ax.set_xlabel("time index")
    ax.set_yticks([])
    ax.grid(False)
    for spine in ("left", "top", "right"):
        ax.spines[spine].set_visible(False)
    ax.set_title("Anchored walk-forward scheme")
    return ax


def plot_permutation_example(
    df_real: pd.DataFrame,
    df_perm: pd.DataFrame,
    start_idx: int,
    ax: plt.Axes | None = None,
):
    """Overlay real vs one permuted price path to make the null tangible."""
    use_academic_style()
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 3.8))

    log_real = np.log(df_real["Close"])
    log_perm = np.log(df_perm["Close"])
    boundary = df_real.index[start_idx]

    ax.plot(log_real.index, log_real, color=PALETTE["real"], linewidth=1.2,
            label="Real log-price")
    ax.plot(log_perm.index, log_perm, color=PALETTE["null"], linewidth=1.0,
            alpha=0.85, label="One permuted path")
    ax.axvline(boundary, color=PALETTE["muted"], linestyle="--", linewidth=0.8)
    ax.text(
        boundary, ax.get_ylim()[1],
        "  permutation boundary",
        color=PALETTE["muted"], fontsize=9,
        ha="left", va="top",
    )

    ax.set_ylabel("log Close")
    ax.set_title("Bar permutation à la Aronson — real vs one realization")
    ax.legend(loc="upper left")
    return ax
