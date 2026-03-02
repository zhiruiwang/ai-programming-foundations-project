"""
Data cleaning functions for PLACES and ACS county data.
"""
import re
import pandas as pd
import numpy as np


def standardize_county_fips(df: pd.DataFrame, fips_column: str) -> pd.DataFrame:
    """
    Standardize county FIPS to zero-padded 5-character string and drop invalid rows.

    Handles GEO_ID format (e.g., 0500000US01001) by extracting the 5-digit county FIPS
    after "US", or converts numeric/string FIPS to 5-digit zero-padded form.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing a FIPS or GEO_ID column.
    fips_column : str
        Name of the column containing FIPS or GEO_ID.

    Returns
    -------
    pd.DataFrame
        Copy of df with a new column 'county_fips' (5-char) and rows with invalid
        FIPS dropped.
    """
    df = df.copy()
    raw = df[fips_column].astype(str).str.strip()

    def extract_fips(s):
        s = str(s).strip()
        if "US" in s.upper():
            match = re.search(r"US(\d{5})", s, re.IGNORECASE)
            if match:
                return match.group(1)
            match = re.search(r"US(\d+)", s, re.IGNORECASE)
            if match:
                return match.group(1).zfill(5)[:5]
        if s.isdigit():
            return s.zfill(5)[:5]
        return None

    df["county_fips"] = raw.map(extract_fips)
    valid = df["county_fips"].notna() & (df["county_fips"].str.len() == 5)
    return df.loc[valid].reset_index(drop=True)


def coerce_numeric(df: pd.DataFrame, columns: list, na_values=None) -> pd.DataFrame:
    """
    Coerce specified columns to numeric, handling common suppressed/missing markers.

    Replaces values like "Data Not Available", "N", "NaN", "~", "-", "(X)" with
    NaN before conversion so they become numeric NaN.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to modify.
    columns : list of str
        Column names to coerce to numeric.
    na_values : list, optional
        Additional strings to treat as NA. Defaults to common Census/PLACES markers.

    Returns
    -------
    pd.DataFrame
        Copy of df with specified columns as numeric (float).
    """
    if na_values is None:
        na_values = [
            "", "NA", "N/A", "NaN", "nan", "None",
            "Data Not Available", "N", "~", "-", "(X)", "**", "***", "*****",
            "median-", "median+", "null",
        ]
    df = df.copy()
    for col in columns:
        if col not in df.columns:
            continue
        s = df[col].astype(str).str.strip()
        for v in na_values:
            s = s.replace(v, np.nan)
        df[col] = pd.to_numeric(s, errors="coerce")
    return df


def filter_places_measure(df: pd.DataFrame, measure_ids: list) -> pd.DataFrame:
    """
    Filter PLACES long-format data to selected measure IDs.

    Parameters
    ----------
    df : pd.DataFrame
        PLACES DataFrame with a 'MeasureId' column.
    measure_ids : list of str
        MeasureId values to keep (e.g., ['OBESITY', 'DIABETES']).

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame.
    """
    return df.loc[df["MeasureId"].isin(measure_ids)].copy()


def pivot_places_wide(df: pd.DataFrame, value_col: str = "Data_Value",
                      index_col: str = "LocationID", aggfunc: str = "mean") -> pd.DataFrame:
    """
    Pivot PLACES from long (one row per county per measure) to wide (one row per county).

    Columns become measure IDs or short names; values are the selected value column.

    Parameters
    ----------
    df : pd.DataFrame
        Long-format PLACES data with MeasureId and value column.
    value_col : str
        Column to use as values in the pivot.
    index_col : str
        Column to use as index (county identifier).
    aggfunc : str
        Aggregation if duplicate (county, measure) exist: 'mean' or 'first'.

    Returns
    -------
    pd.DataFrame
        Wide DataFrame with one row per county.
    """
    wide = df.pivot_table(
        index=index_col,
        columns="MeasureId",
        values=value_col,
        aggfunc=aggfunc,
    )
    return wide.reset_index()


def resolve_duplicates_on_key(df: pd.DataFrame, key_cols: list, method: str = "mean") -> pd.DataFrame:
    """
    Resolve duplicate rows by key columns by aggregating numeric columns.

    If method is 'mean', numeric columns (other than key_cols) are averaged;
    if 'first', the first row is kept.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame that may have duplicate keys.
    key_cols : list of str
        Column(s) that together form the unique key.
    method : str
        'mean' to average numeric cols, 'first' to keep first occurrence.

    Returns
    -------
    pd.DataFrame
        DataFrame with one row per unique key.
    """
    if method == "first":
        return df.drop_duplicates(subset=key_cols, keep="first").reset_index(drop=True)
    agg = {c: "mean" for c in df.select_dtypes(include=[np.number]).columns if c not in key_cols}
    if not agg:
        return df.drop_duplicates(subset=key_cols, keep="first").reset_index(drop=True)
    for c in key_cols:
        if c in df.columns and c not in agg:
            agg[c] = "first"
    return df.groupby(key_cols, as_index=False).agg(agg)
