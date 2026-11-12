# EconScope – Economic Indicator Dictionary

## Overview

EconScope uses macroeconomic indicators retrieved from the World Bank Open Data API. This document provides definitions, indicator codes, units of measurement, and interpretation guidelines for the economic variables used in the dashboard.

## 1. GDP Growth

- **Indicator Name:** GDP Growth (Annual %)
- **World Bank Indicator Code:** `NY.GDP.MKTP.KD.ZG`
- **Unit:** Percentage (%)
- **Description:** Measures the annual percentage growth rate of a country's Gross Domestic Product (GDP) at market prices, adjusted for inflation.
- **Interpretation:**
  - Positive values indicate economic expansion.
  - Negative values indicate economic contraction.
  - Higher values generally indicate faster real economic growth.

## 2. Inflation

- **Indicator Name:** Inflation, Consumer Prices (Annual %)
- **World Bank Indicator Code:** `FP.CPI.TOTL.ZG`
- **Unit:** Percentage (%)
- **Description:** Measures the annual percentage change in the consumer price index (CPI), reflecting changes in the general price level of goods and services.
- **Interpretation:**
  - Positive values indicate an increase in consumer prices.
  - Higher values indicate faster price increases.
  - Negative values indicate deflation.

## 3. Unemployment

- **Indicator Name:** Unemployment, Total (% of Total Labour Force)
- **World Bank Indicator Code:** `SL.UEM.TOTL.ZS`
- **Unit:** Percentage of total labour force (%)
- **Description:** Represents the share of the labour force that is without work but available for and seeking employment.
- **Interpretation:**
  - Higher values indicate a larger proportion of the labour force is unemployed.
  - Lower values generally indicate lower measured unemployment.

## 4. GDP Per Capita

- **Indicator Name:** GDP Per Capita (Current US$)
- **World Bank Indicator Code:** `NY.GDP.PCAP.CD`
- **Unit:** Current US dollars (US$)
- **Description:** Measures a country's total GDP divided by its population, expressed in current US dollars.
- **Interpretation:**
  - Higher values indicate higher GDP per person in current US-dollar terms.
  - Changes can reflect economic growth, population changes, inflation, and exchange-rate movements.
  - It does not directly measure income distribution or individual living standards.

## Data Source

**Primary Source:** World Bank Open Data

**API Endpoint:**

`https://api.worldbank.org/v2/`

**Data Access:** EconScope retrieves annual country-level observations through the World Bank API.

## Important Methodological Notes

1. GDP Growth and Inflation are expressed as annual percentages.
2. Unemployment is measured as a percentage of the total labour force.
3. GDP Per Capita is expressed in current US dollars and is not adjusted for inflation.
4. Missing observations are treated as unavailable data, not as zero.
5. Cross-country comparisons should consider differences in economic structure, population, price levels, and exchange rates.
6. The indicators are intended for exploratory economic analysis and should not independently be interpreted as comprehensive measures of economic welfare.

---

*Documentation for EconScope | Interactive Economics Dashboard*