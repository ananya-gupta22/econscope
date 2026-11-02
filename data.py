
import requests
import pandas as pd

# World Bank API indicator codes
INDICATORS = {
    "GDP Growth": "NY.GDP.MKTP.KD.ZG",
    "Inflation": "FP.CPI.TOTL.ZG",
    "Unemployment": "SL.UEM.TOTL.ZS",
    "GDP Per Capita": "NY.GDP.PCAP.CD"
}


def get_world_bank_data(country_code, indicator_code,
                        start_year=2010, end_year=2024):

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
            return pd.DataFrame()

        records = result[1]

        if not records:
            return pd.DataFrame()

        data = []

        for item in records:
            if item["value"] is not None:
                data.append({
                    "Year": int(item["date"]),
                    "Value": item["value"]
                })

        df = pd.DataFrame(data)

        if not df.empty:
            df = df.sort_values("Year")

        return df

    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"Error retrieving World Bank data: {error}")
        return pd.DataFrame()
