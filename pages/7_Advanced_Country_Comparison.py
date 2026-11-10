
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Load shared dashboard settings
indicator, start_year, end_year = setup_page()

# Page heading
st.title("📊 Advanced Country Comparison")

st.write(
    "Compare multiple economic indicators across countries "
    "using standardised values."
)

# Available indicators
comparison_indicators = [
    name for name in [
        "GDP Growth",
        "GDP Per Capita",
        "Inflation",
        "Unemployment"
    ]
    if name in INDICATORS
]

# Select countries and indicators
col1, col2 = st.columns(2)

with col1:
    advanced_countries = st.multiselect(
        "Select countries",
        options=list(COUNTRIES.keys()),
        default=["India", "Nigeria", "United States"],
        key="advanced_countries"
    )

with col2:
    advanced_indicators = st.multiselect(
        "Select economic indicators",
        options=comparison_indicators,
        default=comparison_indicators,
        key="advanced_indicators"
    )

# Validate year range before displaying year selector
if start_year >= end_year:

    st.warning("Please select a valid year range using the sidebar.")

else:

    advanced_year = st.selectbox(
        "Select comparison year",
        options=list(range(start_year, end_year + 1)),
        index=end_year - start_year,
        key="advanced_comparison_year"
    )

    if len(advanced_countries) < 2:

        st.warning("Please select at least two countries.")

    elif len(advanced_indicators) < 2:

        st.warning("Please select at least two indicators.")

    else:

        advanced_data = []

        # Retrieve data
        with st.spinner("Collecting comparison data..."):

            for selected_country in advanced_countries:

                selected_code = COUNTRIES[selected_country]

                for selected_indicator in advanced_indicators:

                    temp_df = get_world_bank_data(
                        selected_code,
                        INDICATORS[selected_indicator],
                        start_year,
                        end_year
                    )

                    if not temp_df.empty:

                        temp_df["Year"] = pd.to_numeric(
                            temp_df["Year"],
                            errors="coerce"
                        )

                        temp_df["Value"] = pd.to_numeric(
                            temp_df["Value"],
                            errors="coerce"
                        )

                        year_data = temp_df[
                            temp_df["Year"] == advanced_year
                        ]

                        if not year_data.empty:

                            advanced_data.append({
                                "Country": selected_country,
                                "Indicator": selected_indicator,
                                "Year": advanced_year,
                                "Value": year_data.iloc[-1]["Value"]
                            })

        # Process comparison data
        if advanced_data:

            advanced_df = pd.DataFrame(advanced_data)

            advanced_pivot = advanced_df.pivot_table(
                index="Country",
                columns="Indicator",
                values="Value",
                aggfunc="first"
            )

            # Calculate standardised values (Z-scores)
            standardised_data = advanced_pivot.copy()

            for column in standardised_data.columns:

                column_mean = standardised_data[column].mean()
                column_std = standardised_data[column].std(ddof=0)

                if pd.isna(column_std) or column_std == 0:

                    standardised_data[column] = 0

                else:

                    standardised_data[column] = (
                        standardised_data[column] - column_mean
                    ) / column_std

            standardised_long = (
                standardised_data
                .reset_index()
                .melt(
                    id_vars="Country",
                    var_name="Indicator",
                    value_name="Standardised Value"
                )
            )

            if standardised_long["Country"].nunique() >= 2:

                st.subheader(
                    f"Standardised Economic Comparison — {advanced_year}"
                )

                # Grouped bar chart
                advanced_fig = px.bar(
                    standardised_long,
                    x="Country",
                    y="Standardised Value",
                    color="Indicator",
                    barmode="group",
                    title="Comparison of Economic Indicators",
                    hover_data={
                        "Standardised Value": ":.2f"
                    }
                )

                advanced_fig.update_layout(
                    template="plotly_white",
                    xaxis_title="Country",
                    yaxis_title="Standardised Value (Z-score)",
                    legend_title="Economic Indicators"
                )

                st.plotly_chart(
                    advanced_fig,
                    use_container_width=True
                )

                st.caption(
                    "Positive z-scores indicate values above the "
                    "selected countries' average for that indicator; "
                    "negative scores indicate values below the average. "
                    "Each indicator is standardised separately."
                )

                # Original values
                st.subheader("Original Economic Values")

                st.dataframe(
                    advanced_pivot.style.format("{:,.2f}"),
                    use_container_width=True
                )

                # Standardised values
                with st.expander("View Standardised Comparison Data"):

                    st.dataframe(
                        standardised_data.style.format("{:.2f}"),
                        use_container_width=True
                    )

                # Download data
                advanced_csv = advanced_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "⬇️ Download Advanced Comparison Data",
                    data=advanced_csv,
                    file_name="EconScope_Advanced_Comparison.csv",
                    mime="text/csv"
                )

            else:

                st.warning(
                    "Not enough countries have available data "
                    "for the selected indicators and year."
                )

        else:

            st.warning(
                "No data is available for the selected countries, "
                "indicators and year."
            )
