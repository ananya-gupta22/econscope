# 📊 EconScope – Interactive Economics Dashboard

**Explore. Analyse. Understand the Economy.**

EconScope is an interactive economics dashboard built using Python and Streamlit. It enables users to explore macroeconomic indicators, compare economic performance across countries, analyse statistical relationships, conduct exploratory econometric analysis and visualise global economic trends using World Bank data.

The project combines economic concepts, data analytics and statistical techniques to make macroeconomic information more accessible and easier to interpret.

---

## 🌍 Project Overview

EconScope is an independent economics and data analytics project focused on the exploration of macroeconomic indicators through interactive visualisations and statistical tools.

The dashboard provides an environment to:

- Examine the historical performance of individual economies.
- Compare macroeconomic indicators across countries.
- Identify relationships between economic variables.
- Conduct descriptive and econometric analysis.
- Evaluate the availability and completeness of economic data.
- Generate insights from historical economic trends.

## 🖥️ Dashboard Preview

### Home Page
![EconScope Home](screenshots/home.png)

### Country Comparison
![Country Comparison](screenshots/country_comparison.png)

### Econometric Regression Analysis
![Regression Analysis](screenshots/regression_analysis.png)

### Data Quality Overview
![Data Quality Overview](screenshots/data_quality.png)

---

## 🚀 Key Features

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
- Regression Coefficient and P-value Interpretation
- Econometric Diagnostic Tests:
  - Durbin–Watson Test
  - Jarque–Bera Test
  - Breusch–Pagan Test
  - Variance Inflation Factor (VIF)
- Residual Analysis
- Economic Time-Series Analysis
- Automated Economic Insights

### 3. Data Quality and Reliability

- Overall Data Coverage Assessment
- Country-Level Data Availability
- Indicator-Level Coverage Comparison
- Missing Observation Identification
- Data Coverage Heatmap
- Downloadable Data Quality Reports

### 4. Interactive Visualisation

- Interactive line charts
- Country comparison charts
- Global choropleth maps
- Scatter plots with regression trendlines
- Residual plots
- Statistical tables
- CSV data exports

---

## 🌐 Countries Covered

The current dashboard includes ten countries:

1. India
2. Nigeria
3. United States
4. United Kingdom
5. China
6. Germany
7. Japan
8. Brazil
9. France
10. South Africa

Country coverage may be expanded in future versions.

## 📈 Economic Indicators

EconScope currently uses four major macroeconomic indicators from the World Bank.

| Indicator | World Bank Code | Unit |
|---|---|---|
| GDP Growth | NY.GDP.MKTP.KD.ZG | Annual percentage |
| Inflation | FP.CPI.TOTL.ZG | Annual percentage |
| Unemployment | SL.UEM.TOTL.ZS | Percentage of total labour force |
| GDP Per Capita | NY.GDP.PCAP.CD | Current US dollars |

**Data Source:** [World Bank Open Data](https://data.worldbank.org/)

**API Documentation:** [World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589)

Data are retrieved through the World Bank API. Availability varies across countries, indicators and years.

## 📊 Statistical and Econometric Methodology

The dashboard incorporates the following analytical methods:

| Method | Application |
|---|---|
| Descriptive Statistics | Mean, median, standard deviation, minimum and maximum |
| Pearson Correlation | Examining linear relationships between variables |
| Z-score Standardisation | Comparing indicators measured on different scales |
| OLS Regression | Estimating relationships between GDP growth, inflation and unemployment |
| Durbin–Watson Test | Assessing first-order residual autocorrelation |
| Jarque–Bera Test | Examining residual normality |
| Breusch–Pagan Test | Testing for heteroskedasticity |
| VIF | Assessing multicollinearity |
| Time-Series Analysis | Examining historical economic trends |

### Regression Model

The current econometric module estimates the following model:

GDP Growth = β₀ + β₁(Inflation) + β₂(Unemployment) + ε

GDP growth is the dependent variable, while inflation and unemployment are the explanatory variables.

The model uses Ordinary Least Squares (OLS) estimation.

**Important:** Regression results are exploratory statistical estimates. They should not be interpreted as causal effects without further econometric investigation.

---

## 🛠️ Technology Stack

- **Python** – Programming and application logic
- **Streamlit** – Interactive dashboard development
- **Pandas** – Data manipulation and analysis
- **Plotly** – Interactive data visualisation
- **Statsmodels** – Statistical and econometric modelling
- **Requests** – API integration
- **World Bank API** – Macroeconomic data source
- **Git and GitHub** – Version control and project management

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Internet connection

### 1. Clone the repository

```bash
git clone https://github.com/ananya-gupta22/econscope.git
```

### 2. Navigate to the project folder

```bash
cd econscope
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your default browser.

---

## 📁 Project Structure

```text
EconScope/
│
├── app.py
├── common.py
├── data.py
├── requirements.txt
├── README.md
├── .gitignore
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
    ├── 10_Time_Series_and_Insights.py
    └── 11_Data_Quality_Overview.py
```

## 🔎 Data Handling

EconScope retrieves annual economic observations from the World Bank API.

The application incorporates:

- API request handling and timeout controls.
- Data cleaning and numeric conversion.
- Merging of datasets by year.
- Missing-value handling in analytical modules.
- One-hour caching to reduce repeated API requests.
- CSV downloads for selected analytical datasets.

Missing observations are not treated as zero. Analyses that combine multiple indicators use overlapping available observations where required.

## ⚠️ Limitations and Interpretation

- The current dashboard covers ten selected countries.
- Data availability varies by country, indicator and year.
- Missing observations may affect sample sizes and comparisons.
- Correlation does not imply causation.
- OLS estimates are exploratory and should not be interpreted as causal effects.
- Small annual samples may limit the reliability and statistical power of diagnostic tests.
- Passing a diagnostic test does not prove that every model assumption holds.
- Data coverage measures availability, not the accuracy of the underlying economic estimates.

## 🔮 Future Improvements

- Expand geographical coverage.
- Introduce additional macroeconomic and financial indicators.
- Incorporate advanced econometric models.
- Improve data validation and quality assessment.
- Add further interactive visualisations.
- Deploy the application online.
- Expand analytical and forecasting capabilities.

## 🎯 Project Objective

EconScope is an ongoing independent project developed to strengthen practical knowledge and skills in economics, data analysis, Python programming, data visualisation and econometric applications.

It reflects an interest in using data-driven methods to understand economic performance and interpret real-world macroeconomic trends.

---

**Project:** EconScope – Interactive Economics Dashboard  
**Data Source:** World Bank Open Data  
**Repository:** https://github.com/ananya-gupta22/econscope

*Developed as an independent economics and data analytics project.*