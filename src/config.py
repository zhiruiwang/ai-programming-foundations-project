"""
Project configuration: paths, seeds, and selected analysis measures.
"""
import os

# Reproducibility
RANDOM_SEED = 42

# Paths (relative to project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(PROJECT_ROOT, "Data", "Raw")
DATA_PROCESSED = os.path.join(PROJECT_ROOT, "Data", "processed")
OUTPUTS_FIGURES = os.path.join(PROJECT_ROOT, "outputs", "figures")

# Raw data filenames
PLACES_FILENAME = "PLACES__Local_Data_for_Better_Health__County_Data_2024_release.csv"
ACS_B19013_DIR = "ACSDT5Y2024.B19013_2026-03-01T180214"
ACS_B19013_DATA = "ACSDT5Y2024.B19013-Data.csv"

# PLACES measures to analyze (3-6 measures; SES-related and interpretable)
SELECTED_MEASURE_IDS = [
    "OBESITY",      # Obesity among adults
    "DIABETES",     # Diagnosed diabetes among adults
    "BPHIGH",       # High blood pressure among adults
    "DEPRESSION",   # Depression among adults
    "ARTHRITIS",    # Arthritis among adults
]

# Prefer age-adjusted when available for comparability across counties
DATA_VALUE_TYPE_PREFER = "AgeAdjPrv"
