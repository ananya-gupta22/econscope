
import streamlit as st
import pandas as pd

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Load shared dashboard settings
indicator, start_year, end_year = setup_page()

# Page heading
st.title("🌐 Economic Performance Scorecard")

st.write(
    "A consolidated overview of a country's "
    "major macroeconomic indicators."
)

# Country selection
country = st.selectbox(
    "Select a country",
    list(COUNTRIES.keys())
)

country_code = COUNTRIES[country]

# Indicators included in the scorecard
scorecard_indicators = [
    "GDP Growth",
    "GDP Per Capita",
    "Inflation",
    "Unemployment"
]

scorecard_data = {}

# Retrieve economic data
if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    with st.spinner("Preparing country economic scorecard..."):

        for name in scorecard_indicators:

            if name in INDICATORS:

                score_df = get_world_bank_data(
                    country_code,
                    INDICATORS[name],
                    start_year,
                    end_year
                )

                if not score_df.empty:

                    score_df = score_df.copy()

                    score_df["Year"] = pd.to_numeric(
                        score_df["Year"],
                        errors="coerce"
                    )

                    score_df["Value"] = pd.to_numeric(
                        score_df["Value"],
                        errors="coerce"
                    )

                    score_df = score_df.dropna(
                        subset=["Year", "Value"]
                    ).sort_values("Year")

                    if not score_df.empty:

                        latest_row = score_df.iloc[-1]

                        previous_value = (
                            score_df.iloc[-2]["Value"]
                            if len(score_df) > 1
                            else None
                        )

                        scorecard_data[name] = {
                            "Value": latest_row["Value"],
                            "Year": int(latest_row["Year"]),
                            "Previous": previous_value
                        }

    if scorecard_data:

        st.subheader(f"Economic Profile: {country}")

        # Display four economic indicators
        col1, col2, col3, col4 = st.columns(4)

        columns = [col1, col2, col3, col4]

        for column, name in zip(
            columns,
            scorecard_indicators
        ):

            with column:

                if name in scorecard_data:

                    item = scorecard_data[name]

                    value = item["Value"]

                    formatted_value = (
                        f"${value:,.2f}"
                        if name == "GDP Per Capita"
                        else f"{value:,.2f}%"
                    )

                    delta = None

                    if item["Previous"] is not None:

                        change = value - item["Previous"]

                        delta = f"{change:+,.2f}"

                    st.metric(
                        label=name,
                        value=formatted_value,
                        delta=delta,
                        help=(
                            f"Latest available observation: "
                            f"{item['Year']}. Delta represents "
                            f"the difference from the previous "
                            f"available observation."
                        )
                    )

                else:

                    st.metric(
                        label=name,
                        value="N/A"
                    )

        st.divider()

        # Detailed economic profile
        st.subheader("Detailed Economic Profile")

        profile_rows = []

        for name in scorecard_indicators:

            if name in scorecard_data:

                item = scorecard_data[name]

                profile_rows.append({
                    "Economic Indicator": name,
                    "Latest Value": item["Value"],
                    "Latest Year": item["Year"],
                    "Previous Observation": (
                        item["Previous"]
                        if item["Previous"] is not None
                        else "N/A"
                    )
                })

        profile_df = pd.DataFrame(profile_rows)

        st.dataframe(
            profile_df,
            use_container_width=True,
            hide_index=True
        )

        # CSV download
        profile_csv = profile_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Economic Profile",
            data=profile_csv,
            file_name=f"EconScope_{country}_Economic_Profile.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No economic indicators are available for this selection."
        )
