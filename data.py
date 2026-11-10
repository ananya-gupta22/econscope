
import requests
import pandas as pd
import streamlit as st


# World Bank API indicator codes
INDICATORS = {
    "GDP Growth": "NY.GDP.MKTP.KD.ZG",
    "Inflation": "FP.CPI.TOTL.ZG",
    "Unemployment": "SL.UEM.TOTL.ZS",
    "GDP Per Capita": "NY.GDP.PCAP.CD"
}


@st.cache_data(ttl=3600, show_spinner=False)
def get_world_bank_data(
    country_code,
    indicator_code,
    start_year=2010,
    end_year=2024
):
    """
    Retrieve annual economic data from the World Bank API.

    Cached for one hour to reduce repeated API requests.
    Returns a DataFrame with Year and Value columns.
    """

    url = (
        f"https://api.worldbank.org/v2/country/"
        f"{country_code}/indicator/{indicator_code}"
    )

    params = {
        "date": f"{start_year}:{end_year}",
        "format": "json",
        "per_page": 100
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()
        result = response.json()

        if not isinstance(result, list) or len(result) < 2:
            return pd.DataFrame(columns=["Year", "Value"])

        records = result[1]

        if not isinstance(records, list):
            return pd.DataFrame(columns=["Year", "Value"])

        data = []

        for item in records:

            if not isinstance(item, dict):
                continue

            value = item.get("value")
            year = item.get("date")

            if value is None or year is None:
                continue

            try:
                data.append({
                    "Year": int(year),
                    "Value": float(value)
                })
            except (ValueError, TypeError):
                continue

        df = pd.DataFrame(
            data,
            columns=["Year", "Value"]
        )

        if not df.empty:
            df = df.sort_values("Year").reset_index(drop=True)

        return df

    except (requests.RequestException, ValueError, TypeError) as error:

        print(f"Error retrieving World Bank data: {error}")

        return pd.DataFrame(columns=["Year", "Value"])

