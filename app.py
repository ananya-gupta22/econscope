
import streamlit as st
from common import setup_page

# Shared dashboard settings
indicator, start_year, end_year = setup_page()

# --------------------------------
# HOME PAGE
# --------------------------------

st.title("📊 EconScope")

st.subheader("Explore. Analyse. Understand the Economy.")

st.markdown(
    """
    EconScope is an interactive economics dashboard designed
    to explore macroeconomic indicators, compare countries,
    identify economic relationships and understand global
    economic trends using World Bank data.
    """
)

st.divider()

# --------------------------------
# PROJECT OVERVIEW
# --------------------------------

st.header("Your Economics Research Workspace")

st.write(
    "Use the navigation menu on the left to access different "
    "analytical tools and explore economic data."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Analysis Modules", "10")

with col2:
    st.metric("Countries Available", "10")

with col3:
    st.metric("Primary Data Source", "World Bank")

st.divider()

# --------------------------------
# AVAILABLE FEATURES
# --------------------------------

st.header("Explore the Dashboard")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🌍 Economic Data Exploration")

    st.markdown(
        """
        - Individual Country Analysis
        - Country Comparison
        - Country Rankings
        - Economic Performance Scorecard
        - Global Economic Map
        """
    )

with col2:

    st.subheader("📈 Statistical & Econometric Tools")

    st.markdown(
        """
        - Economic Relationship Analysis
        - Advanced Country Comparison
        - Statistical Analysis
        - Econometric Regression Analysis
        - Time-Series Analysis and Insights
        """
    )

st.divider()

# --------------------------------
# RESEARCH METHODOLOGY
# --------------------------------

st.header("Data and Methodology")

st.markdown(
    """
    **Data Source:** World Bank Open Data.

    **Analytical Methods:**
    - Descriptive statistics
    - Pearson correlation analysis
    - Standardisation using Z-scores
    - Ordinary Least Squares (OLS) regression
    - Historical time-series analysis

    **Purpose:** To make economic data easier to explore,
    compare and interpret through interactive visualisations
    and statistical tools.
    """
)

st.info(
    "Select an analysis module from the sidebar to begin "
    "exploring economic indicators."
)

st.divider()

# --------------------------------
# FOOTER
# --------------------------------

st.caption(
    "EconScope | Independent Economics Dashboard Project"
)

st.caption(
    "Data Source: World Bank Open Data | "
    "Results are intended for exploratory and educational analysis."
)
