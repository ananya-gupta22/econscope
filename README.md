# EconScope – Interactive Economics Dashboard

An interactive economics dashboard built using Python and Streamlit to explore macroeconomic indicators, compare countries, analyse economic relationships, and visualise global economic trends using World Bank data.

## Project Overview

EconScope is an independent data analytics project designed to make macroeconomic data more accessible through interactive visualisations and statistical analysis.

The dashboard allows users to examine economic indicators across countries, identify historical patterns, compare economic performance, and explore relationships between key macroeconomic variables.

## Key Features

### 1. Economic Data Exploration

- Individual Country Analysis
- Country Comparison
- Country Rankings
- Economic Performance Scorecard
- Global Economic Map

### 2. Statistical and Econometric Analysis

- Economic Relationship Analysis
- Advanced Country Comparison using Z-scores
- Descriptive Statistical Analysis
- Pearson Correlation Analysis
- Ordinary Least Squares (OLS) Regression
- Economic Time-Series Analysis
- Automated Economic Insights

## Countries Covered

The current dashboard includes:

- India
- Nigeria
- United States
- United Kingdom
- China
- Germany
- Japan
- Brazil
- France
- South Africa

## Data Source

The dashboard retrieves economic indicators from the **World Bank Open Data API**.

Source: [https://data.worldbank.org/](https://data.worldbank.org/)

Data availability varies by country and indicator. Missing observations are excluded from relevant analyses.

## Technology Stack

- **Python** – Data processing and application logic
- **Streamlit** – Interactive dashboard interface
- **Pandas** – Data manipulation and analysis
- **Plotly** – Interactive charts and visualisations
- **Statsmodels** – Econometric regression analysis
- **Requests** – API integration
- **World Bank API** – Macroeconomic data source

## Statistical Methods

The project uses:

- Mean, median, standard deviation, minimum and maximum
- Pearson correlation coefficients
- Z-score standardisation
- Ordinary Least Squares regression
- Historical time-series comparisons

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Internet connection

### 1. Clone the repository

```bash
git clone https://github.com/ananya-gupta22/econscope.git
```

### 2. Open the project folder

```bash
cd EconScope
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The application will open in your browser.

## Project Structure

```text
EconScope/
│
├── app.py
├── common.py
├── data.py
├── requirements.txt
├── README.md
│
└── pages/
    ├── 1_Individual_Country_Analysis.py
    ├── 2_Country_Comparison.py
    ├── 3_Country_Rankings.py
    ├── 4_Economic_Performance_Scorecard.py
    ├── 5_Global_Economic_Map.py
    ├── 6_Economic_Relationship_Analysis.py
    ├── 7_Advanced_Country_Comparison.py
    ├── 8_Statistical_Analysis.py
    ├── 9_Econometric_Regression_Analysis.py
    └── 10_Time_Series_and_Insights.py
```

## Limitations and Interpretation

- The dashboard currently covers ten countries.
- Data availability differs across indicators and countries.
- Correlation does not imply causation.
- OLS regression outputs are exploratory and should not be interpreted as causal estimates.
- Small samples and time-series properties may affect statistical results.

## Future Improvements

- Expand country coverage.
- Introduce additional macroeconomic indicators.
- Add more advanced econometric techniques.
- Improve data caching and API efficiency.
- Deploy the dashboard online.
- Add further interactive data visualisations.

## Project Objective

EconScope is an ongoing independent project developed to strengthen practical skills in economics, data analysis, Python programming, and econometric applications.

