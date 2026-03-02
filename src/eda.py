"""
Exploratory data analysis
"""
import pandas as pd
import numpy as np


def run_eda(df: pd.DataFrame, key_id_col: str = "county_fips",
            numeric_cols: list = None) -> dict:
    """
    Run exploratory analysis: shape, missingness, summary stats, top/bottom counties,
    and correlation matrix for numeric columns.

    Parameters
    ----------
    df : pd.DataFrame
        Merged or analysis-ready DataFrame (e.g., one row per county).
    key_id_col : str
        Column identifying the unit (e.g., county_fips).
    numeric_cols : list, optional
        Columns to include in summary and correlation. Defaults to all numeric.

    Returns
    -------
    dict
        Keys: 'shape', 'missing', 'summary', 'correlation', 'top_counties', 'bottom_counties'.
        Values are DataFrames or dicts for use in the notebook.
    """
    out = {}
    out["shape"] = df.shape
    out["missing"] = df.isnull().sum()
    numeric = numeric_cols if numeric_cols is not None else df.select_dtypes(include=[np.number]).columns.tolist()
    numeric = [c for c in numeric if c in df.columns]
    out["summary"] = df[numeric].describe() if numeric else pd.DataFrame()

    if key_id_col in df.columns and numeric:
        # Top/bottom by first numeric (often income)
        first_num = numeric[0]
        sorted_df = df.sort_values(first_num, ascending=False, na_position="last")
        out["top_counties"] = sorted_df[[key_id_col] + numeric].head(10)
        out["bottom_counties"] = sorted_df[[key_id_col] + numeric].tail(10)

    if len(numeric) >= 2:
        out["correlation"] = df[numeric].corr()
    else:
        out["correlation"] = pd.DataFrame()

    return out
