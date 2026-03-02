"""
Data ingestion: load PLACES and ACS B19013 datasets.
"""
import os
import pandas as pd

from .config import (
    DATA_RAW,
    PLACES_FILENAME,
    ACS_B19013_DIR,
    ACS_B19013_DATA,
)


def load_places(data_dir=None) -> pd.DataFrame:
    """
    Load CDC PLACES county-level health data (2024 release).

    Returns a DataFrame with one row per county per measure (long format).
    Columns include LocationID (county FIPS), MeasureId, Data_Value, etc.

    Parameters
    ----------
    data_dir : str, optional
        Directory containing the PLACES CSV. Defaults to config DATA_RAW.

    Returns
    -------
    pd.DataFrame
    """
    data_dir = data_dir or DATA_RAW
    path = os.path.join(data_dir, PLACES_FILENAME)
    return pd.read_csv(path, low_memory=False)


def load_acs_income(data_dir=None) -> pd.DataFrame:
    """
    Load ACS 5-year B19013 median household income by county.

    Returns a DataFrame with GEO_ID, NAME, estimate (B19013_001E),
    and margin of error (B19013_001M). County FIPS must be extracted from GEO_ID
    (e.g., 0500000US01001 -> 01001).

    Parameters
    ----------
    data_dir : str, optional
        Directory containing the ACS B19013 folder. Defaults to config DATA_RAW.

    Returns
    -------
    pd.DataFrame
    """
    data_dir = data_dir or DATA_RAW
    path = os.path.join(data_dir, ACS_B19013_DIR, ACS_B19013_DATA)
    df = pd.read_csv(path)
    # Census export sometimes has a second header row (e.g. "Geography"); drop it
    if len(df) > 0 and str(df.iloc[0].get("GEO_ID", "")).startswith("Geography"):
        df = df.iloc[1:].reset_index(drop=True)
    return df
