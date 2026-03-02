# AI Programming Foundations Project: County Level Income and Health Data Workflow

## Project Description

This repository contains a reproducible data workflow that links U.S. county-level median household income (American Community Survey, ACS B19013) with selected health outcome estimates from CDC PLACES. The project loads, cleans, merges, and visualizes the two datasets to explore how socioeconomic conditions relate to health at the county level.

## Libraries and Tools

- **Python**, **NumPy**, **Pandas**, **Matplotlib**, **Seaborn**, **Jupyter** (for the notebook), and **Git** for version control. All are required by the project; install via `pip install -r requirements.txt`.

## Data Sources

- **CDC PLACES — Local Data for Better Health, County Data 2024 release**  
  County-level model-based estimates of health outcomes and risk factors (e.g., obesity, diabetes) from the Behavioral Risk Factor Surveillance System (BRFSS).  
  Source: [CDC PLACES / Chronic Data](https://catalog.data.gov/dataset/places-local-data-for-better-health-county-data-2024-release).  
  File: `Data/Raw/PLACES__Local_Data_for_Better_Health__County_Data_2024_release.csv`

- **U.S. Census Bureau, American Community Survey (ACS) 5-Year Estimates**  
  Table B19013: Median household income in the past 12 months (in 2024 inflation-adjusted dollars) by county.  
  Source: [data.census.gov](https://data.census.gov/table/ACSDT5Y2023.B19013) (search for B19013 or ACS 5-Year).  
  Folder: `Data/Raw/ACSDT5Y2024.B19013_2026-03-01T180214/`  
  File: `ACSDT5Y2024.B19013-Data.csv`

## How to Run

1. **Clone the repository** and open a terminal in the project root.

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Open and run the Jupyter notebook:**
   - From the project root, run:
     ```bash
     jupyter notebook data_workflow.ipynb
     ```
   - Open `data_workflow.ipynb` in the browser; run all cells from top to bottom (Cell → Run All).

5. **Outputs:**
   - Processed merged dataset: `Data/processed/merged_county_places_acs.csv`
   - Figures: `outputs/figures/` (scatter, boxplot, correlation heatmap)

## Reproducibility Notes

- **File paths:** All paths are relative to the project root. Run the notebook from the repository root directory.
- **Raw data:** Place the PLACES CSV and the ACS B19013 folder under `Data/Raw/` as indicated above. No renaming of files is required if you use the same download structure.
- **Seed:** A fixed random seed is set in the notebook for reproducibility where applicable.
- **requirements.txt:** Dependencies are listed in `requirements.txt`

## Bias Awareness

- **Cleaning choices:** Dropping counties with missing or suppressed values (e.g., Census “-” or “N”) can introduce **selection bias** if missingness is related to income or health. Counties with very small populations or high uncertainty are more likely to be suppressed; excluding them may underrepresent rural or disadvantaged areas.
- **Ecological fallacy:** All analyses are at the **county level**. Associations between county income and county health do not imply the same relationship at the **individual** level; individual income and health may behave differently.
- **Data quality:** PLACES estimates are model-based and have confidence limits; ACS estimates have margins of error. Interpret findings with these limitations in mind.

## Reflection: Future AI Integration

- **ML workflow changes:** A natural next step would be to define a target (e.g., a binary or continuous health outcome), split data into train/test by time or geography, apply feature scaling, and train predictive models (e.g., regression or classification) with proper validation.
- **Neural network preparation:** For NN-based models, we would consider encoding categorical variables, normalizing/standardizing inputs, and defining a clear strategy for missingness (e.g., imputation or masking).
- **Agentic automation potential:** This workflow could be extended with agentic AI for automatic data refresh (e.g., pulling updated PLACES/ACS releases), generating periodic reports, and running QA checks on data quality and consistency.

## Repository Structure

```
County-Income-and-Health/
├── Data/
│   ├── Raw/                    # PLACES CSV, ACS B19013 folder
│   └── processed/              # merged_county_places_acs.csv
├── outputs/
│   └── figures/                # saved plots
├── src/
│   ├── config.py
│   ├── io.py
│   ├── cleaning.py
│   ├── eda.py
│   └── viz.py
├── data_workflow.ipynb         # main workflow notebook
├── requirements.txt
├── README.md
└── .gitignore
```
