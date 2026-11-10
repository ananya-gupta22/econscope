
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Load shared dashboard settings
indicator, start_year, end_year = setup_page()

indicator_code = INDICATORS[indicator]

# Page heading
st.title("🏆 Global Economic Rankings")

st.write(
    "Rank countries according to their economic indicators "
    "and compare their performance."
)

# Validate year range
if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    # Ranking controls
    ranking_year = st.selectbox(
        "Select Year for Country Rankings",
        list(range(start_year, end_year + 1)),
        index=end_year - start_year,
        key="ranking_year"
    )

    ranking_order = st.radio(
        "Select Ranking Order",
        ["Highest to Lowest", "Lowest to Highest"],
        horizontal=True,
        key="ranking_order"
    )

    ranking_data = []

    # Retrieve country data
    with st.spinner("Calculating country rankings..."):

        for country_name, code in COUNTRIES.items():

            country_df = get_world_bank_data(
                code,
                indicator_code,
                start_year,
                end_year
            )

            if not country_df.empty:

                country_df["Year"] = pd.to_numeric(
                    country_df["Year"],
                    errors="coerce"
                )

                country_df["Value"] = pd.to_numeric(
                    country_df["Value"],
                    errors="coerce"
                )

                selected_year_data = country_df[
                    country_df["Year"] == ranking_year
                ]

                if not selected_year_data.empty:

                    value = selected_year_data.iloc[-1]["Value"]

                    if pd.notna(value):

                        ranking_data.append({
                            "Country": country_name,
                            "Year": ranking_year,
                            "Value": value
                        })

    # Display rankings
    if ranking_data:

        ranking_df = pd.DataFrame(ranking_data)

        ascending_order = (
            ranking_order == "Lowest to Highest"
        )

        ranking_df = ranking_df.sort_values(
            by="Value",
            ascending=ascending_order
        ).reset_index(drop=True)

        ranking_df.insert(
            0,
            "Rank",
            range(1, len(ranking_df) + 1)
        )

        st.subheader(
            f"{indicator} Rankings — {ranking_year}"
        )

        # Summary metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Countries Ranked",
                len(ranking_df)
            )

        with col2:
            st.metric(
                "Top Ranked Country",
                ranking_df.iloc[0]["Country"]
            )

        # Ranking table
        st.dataframe(
            ranking_df.style.format({
                "Value": "{:,.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )

        # Ranking chart
        ranking_fig = px.bar(
            ranking_df,
            x="Value",
            y="Country",
            orientation="h",
            color="Value",
            text_auto=".2f",
            color_continuous_scale="Blues",
            title=f"Country Rankings: {indicator}"
        )

        ranking_fig.update_layout(
            template="plotly_white",
            xaxis_title=indicator,
            yaxis_title="Country",
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            ranking_fig,
            use_container_width=True
        )

        # CSV download
        ranking_csv = ranking_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Country Rankings",
            data=ranking_csv,
            file_name=(
                f"EconScope_{indicator.replace(' ', '_')}"
                f"_Rankings_{ranking_year}.csv"
            ),
            mime="text/csv"
        )

    else:

        st.warning(
            "No ranking data available for the selected year."
        )
