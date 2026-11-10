
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Shared dashboard settings
indicator, start_year, end_year = setup_page()

# Page heading
st.title("📊 Economic Time-Series Analysis")

st.write(
    "Explore historical economic trends, annual changes "
    "and automatically generated insights."
)

# Select country
country = st.selectbox(
    "Select Country",
    list(COUNTRIES.keys()),
    key="timeseries_country"
)

country_code = COUNTRIES[country]

if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    # --------------------------------
    # RETRIEVE TIME-SERIES DATA
    # --------------------------------

    time_series_indicators = [
        "GDP Growth",
        "Inflation",
        "Unemployment",
        "GDP Per Capita"
    ]

    time_series_data = {}

    with st.spinner("Retrieving historical economic data..."):

        for indicator_name in time_series_indicators:

            if indicator_name in INDICATORS:

                ts_df = get_world_bank_data(
                    country_code,
                    INDICATORS[indicator_name],
                    start_year,
                    end_year
                )

                if not ts_df.empty:

                    ts_df = ts_df[
                        ["Year", "Value"]
                    ].copy()

                    ts_df["Year"] = pd.to_numeric(
                        ts_df["Year"],
                        errors="coerce"
                    )

                    ts_df["Value"] = pd.to_numeric(
                        ts_df["Value"],
                        errors="coerce"
                    )

                    ts_df = ts_df.dropna()

                    if not ts_df.empty:
                        time_series_data[indicator_name] = ts_df

    # --------------------------------
    # TIME-SERIES CHARTS
    # --------------------------------

    if time_series_data:

        st.header("Historical Economic Trends")

        for indicator_name, ts_df in time_series_data.items():

            st.subheader(indicator_name)

            fig = px.line(
                ts_df.sort_values("Year"),
                x="Year",
                y="Value",
                markers=True,
                title=f"{indicator_name} — {country}"
            )

            fig.update_layout(
                template="plotly_white",
                xaxis_title="Year",
                yaxis_title=indicator_name,
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------
        # YEAR-ON-YEAR CHANGES
        # --------------------------------

        st.header("Year-on-Year Changes")

        for indicator_name, ts_df in time_series_data.items():

            change_df = ts_df.sort_values("Year").copy()

            change_df["Annual Change"] = (
                change_df["Value"].diff()
            )

            st.markdown(f"**{indicator_name}**")

            st.dataframe(
                change_df.rename(
                    columns={
                        "Year": "Year",
                        "Value": "Indicator Value",
                        "Annual Change": "Change from Previous Available Year"
                    }
                ).style.format({
                    "Indicator Value": "{:,.2f}",
                    "Change from Previous Available Year": "{:,.2f}"
                }),
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------
        # COMPLETE DATASET AND DOWNLOAD
        # --------------------------------

        combined_data = None

        for name, ts_df in time_series_data.items():

            temp = ts_df.rename(
                columns={"Value": name}
            )

            if combined_data is None:

                combined_data = temp

            else:

                combined_data = pd.merge(
                    combined_data,
                    temp,
                    on="Year",
                    how="outer"
                )

        combined_data = combined_data.sort_values("Year")

        with st.expander("View Complete Time-Series Dataset"):

            st.dataframe(
                combined_data,
                use_container_width=True,
                hide_index=True
            )

            csv_data = combined_data.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Time-Series Data",
                data=csv_data,
                file_name="EconScope_Time_Series_Data.csv",
                mime="text/csv"
            )

        # --------------------------------
        # AUTOMATED ECONOMIC INSIGHTS
        # --------------------------------

        st.divider()

        st.header("💡 Automated Economic Insights")

        st.write(
            "Discover important patterns and changes in "
            f"{country}'s economic indicators."
        )

        for indicator_name, ts_df in time_series_data.items():

            insight_df = (
                ts_df[["Year", "Value"]]
                .copy()
                .dropna()
                .sort_values("Year")
            )

            if len(insight_df) >= 2:

                first_value = insight_df.iloc[0]["Value"]
                last_value = insight_df.iloc[-1]["Value"]

                first_year = int(insight_df.iloc[0]["Year"])
                last_year = int(insight_df.iloc[-1]["Year"])

                highest = insight_df.loc[
                    insight_df["Value"].idxmax()
                ]

                lowest = insight_df.loc[
                    insight_df["Value"].idxmin()
                ]

                overall_change = last_value - first_value

                st.subheader(indicator_name)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Starting Value",
                        f"{first_value:,.2f}",
                        help=f"Year: {first_year}"
                    )

                with col2:
                    st.metric(
                        "Latest Value",
                        f"{last_value:,.2f}",
                        help=f"Year: {last_year}"
                    )

                with col3:
                    st.metric(
                        "Overall Change",
                        f"{overall_change:+,.2f}"
                    )

                st.write(
                    f"**Highest observation:** "
                    f"{highest['Value']:,.2f} in "
                    f"{int(highest['Year'])}."
                )

                st.write(
                    f"**Lowest observation:** "
                    f"{lowest['Value']:,.2f} in "
                    f"{int(lowest['Year'])}."
                )

                if overall_change > 0:

                    st.success(
                        f"{indicator_name} increased between "
                        f"{first_year} and {last_year}."
                    )

                elif overall_change < 0:

                    st.info(
                        f"{indicator_name} decreased between "
                        f"{first_year} and {last_year}."
                    )

                else:

                    st.info(
                        f"{indicator_name} remained unchanged "
                        "between the first and last observations."
                    )

                st.divider()

            else:

                st.info(
                    f"Insufficient observations for {indicator_name}."
                )

        st.caption(
            "Insights are generated using observed annual data. "
            "They describe historical changes and do not establish "
            "causal relationships or predict future outcomes."
        )

    else:

        st.warning(
            "No time-series data is currently available "
            "for the selected country and period."
        )

# Footer
st.divider()

st.caption(
    "EconScope | Independent Economics Dashboard Project"
)

st.caption(
    "Source: World Bank Open Data | "
    "Missing observations are excluded from visualisations."
)
