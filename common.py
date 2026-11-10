
import streamlit as st
from data import INDICATORS


# --------------------------------
# COUNTRY INFORMATION
# --------------------------------

COUNTRIES = {
    "India": "IND",
    "Nigeria": "NGA",
    "United States": "USA",
    "United Kingdom": "GBR",
    "China": "CHN",
    "Germany": "DEU",
    "Japan": "JPN",
    "Brazil": "BRA",
    "France": "FRA",
    "South Africa": "ZAF"
}


# --------------------------------
# SHARED PAGE SETUP
# --------------------------------

def setup_page():

    # Page configuration
    st.set_page_config(
        page_title="EconScope | Economics Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # Shared dashboard styling
    st.markdown("""
    <style>

    .stApp {
        background-color: #0B1120;
        color: #E5E7EB;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    [data-testid="stSidebar"] {
        background-color: #111C30;
        border-right: 1px solid #263750;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #60A5FA;
    }

    h1, h2, h3 {
        color: #F8FAFC !important;
    }

    p {
        color: #CBD5E1;
    }

    [data-testid="stMetric"] {
        background-color: #16243A;
        border: 1px solid #263750;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8;
    }

    [data-testid="stMetricValue"] {
        color: #60A5FA;
    }

    .stButton > button,
    .stDownloadButton > button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #1D4ED8;
        color: white;
        border: none;
    }

    hr {
        border-color: #263750;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #263750;
        border-radius: 10px;
    }

    [data-testid="stExpander"] {
        background-color: #111C30;
        border: 1px solid #263750;
        border-radius: 10px;
    }

    [data-testid="stSelectbox"] {
        border-radius: 8px;
    }

    </style>
    """, unsafe_allow_html=True)

    # Shared sidebar controls
    st.sidebar.header("Dashboard Controls")

    indicator = st.sidebar.selectbox(
        "Select Economic Indicator",
        list(INDICATORS.keys())
    )

    start_year = st.sidebar.selectbox(
        "Start Year",
        list(range(2000, 2021)),
        index=10
    )

    end_year = st.sidebar.selectbox(
        "End Year",
        list(range(2015, 2025)),
        index=9
    )

    return indicator, start_year, end_year
