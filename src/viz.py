"""
Visualizations
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_scatter_income_vs_outcome(df: pd.DataFrame, income_col: str, outcome_col: str,
                                   title: str = None, xlabel: str = None, ylabel: str = None,
                                   ax=None, add_trend: bool = True):
    """
    Scatter plot of median income vs one health outcome with optional trend line.

    Parameters
    ----------
    df : pd.DataFrame
        Merged data with income and outcome columns.
    income_col : str
        Column name for median household income.
    outcome_col : str
        Column name for health outcome (e.g., prevalence %).
    title, xlabel, ylabel : str, optional
        Plot labels.
    ax : matplotlib axes, optional
    add_trend : bool
        If True, add a linear trend line.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    clean = df[[income_col, outcome_col]].dropna()
    ax.scatter(clean[income_col], clean[outcome_col], alpha=0.5, s=20)
    if add_trend and len(clean) > 1:
        z = np.polyfit(clean[income_col], clean[outcome_col], 1)
        p = np.poly1d(z)
        x_line = np.linspace(clean[income_col].min(), clean[income_col].max(), 100)
        ax.plot(x_line, p(x_line), "r-", linewidth=2, label="Trend")
        ax.legend()
    ax.set_title(title or f"{outcome_col} vs {income_col}")
    ax.set_xlabel(xlabel or income_col)
    ax.set_ylabel(ylabel or outcome_col)
    return ax


def plot_box_outcome_by_income_quartile(df: pd.DataFrame, income_col: str, outcome_col: str,
                                         quartile_col: str = None, title: str = None,
                                         xlabel: str = None, ylabel: str = None, ax=None):
    """
    Boxplot of health outcome by income quartile.

    If quartile_col is not provided, creates quartiles from income_col using qcut.

    Parameters
    ----------
    df : pd.DataFrame
        Merged data.
    income_col : str
        Column name for median household income.
    outcome_col : str
        Column name for health outcome.
    quartile_col : str, optional
        Pre-computed quartile label column. If None, computed from income_col.
    title, xlabel, ylabel : str, optional
    ax : matplotlib axes, optional
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    plot_df = df[[income_col, outcome_col]].dropna()
    if quartile_col and quartile_col in df.columns:
        plot_df = df[[quartile_col, outcome_col]].dropna()
        qcol = quartile_col
    else:
        plot_df = plot_df.copy()
        try:
            plot_df["income_quartile"] = pd.qcut(plot_df[income_col], 4, labels=["Q1 (low)", "Q2", "Q3", "Q4 (high)"])
        except ValueError:
            plot_df["income_quartile"] = pd.qcut(plot_df[income_col].rank(method="first"), 4, labels=["Q1 (low)", "Q2", "Q3", "Q4 (high)"])
        qcol = "income_quartile"
    sns.boxplot(data=plot_df, x=qcol, y=outcome_col, ax=ax)
    ax.set_title(title or f"{outcome_col} by income quartile")
    ax.set_xlabel(xlabel or "Income quartile")
    ax.set_ylabel(ylabel or outcome_col)
    return ax


def plot_corr_heatmap(corr: pd.DataFrame, title: str = "Correlation matrix", ax=None):
    """
    Heatmap of correlation matrix.

    Parameters
    ----------
    corr : pd.DataFrame
        Correlation matrix (e.g., from run_eda or df.corr()).
    title : str
    ax : matplotlib axes, optional
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, square=True)
    ax.set_title(title)
    return ax
