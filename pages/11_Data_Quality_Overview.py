
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# --------------------------------
# PAGE SETUP
# --------------------------------

indicator, start_year, end_year = setup_page()

st.title("🔍 Data Quality Overview")

st.write(
    "Evaluate the completeness and availability of World Bank "
    "economic data across countries and indicators."
)

# --------------------------------
# YEAR VALIDATION
# --------------------------------

if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    expected_observations = end_year - start_year + 1

    quality_records = []
    missing_records = []

    # --------------------------------
    # DATA COLLECTION
    # --------------------------------

    with st.spinner("Checking data availability across countries..."):

        for country, country_code in COUNTRIES.items():

            for indicator_name, indicator_code in INDICATORS.items():

                df = get_world_bank_data(
                    country_code,
                    indicator_code,
                    start_year,
                    end_year
                )

                if not df.empty:

                    available_years = sorted(
                        df["Year"].dropna().astype(int).unique().tolist()
                    )

                else:

                    available_years = []

                available_count = len(available_years)

                missing_years = sorted(
                    set(range(start_year, end_year + 1))
                    - set(available_years)
                )

                coverage = (
                    available_count / expected_observations
                ) * 100

                quality_records.append({
                    "Country": country,
                    "Indicator": indicator_name,
                    "Expected Observations": expected_observations,
                    "Available Observations": available_count,
                    "Missing Observations": len(missing_years),
                    "Data Coverage (%)": coverage
                })

                missing_records.append({
                    "Country": country,
                    "Indicator": indicator_name,
                    "Missing Years": (
                        ", ".join(map(str, missing_years))
                        if missing_years
                        else "None"
                    )
                })

    # --------------------------------
    # QUALITY DATAFRAME
    # --------------------------------

    quality_df = pd.DataFrame(quality_records)

    missing_df = pd.DataFrame(missing_records)

    # --------------------------------
    # OVERALL DATA QUALITY
    # --------------------------------

    total_expected = quality_df[
        "Expected Observations"
    ].sum()

    total_available = quality_df[
        "Available Observations"
    ].sum()

    total_missing = quality_df[
        "Missing Observations"
    ].sum()

    overall_coverage = (
        total_available / total_expected * 100
        if total_expected > 0
        else 0
    )

    st.header("Overall Data Coverage")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Overall Coverage",
            f"{overall_coverage:.1f}%"
        )

    with col2:
        st.metric(
            "Expected Observations",
            int(total_expected)
        )

    with col3:
        st.metric(
            "Available Observations",
            int(total_available)
        )

    with col4:
        st.metric(
            "Missing Observations",
            int(total_missing)
        )

    st.progress(
        int(round(overall_coverage))
    )

    st.divider()

    # --------------------------------
    # COUNTRY-INDICATOR DATA TABLE
    # --------------------------------

    st.header("Country-Level Data Availability")

    st.dataframe(
        quality_df.style.format({
            "Data Coverage (%)": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------
    # COVERAGE HEATMAP
    # --------------------------------

    st.header("Data Coverage Heatmap")

    heatmap_df = quality_df.pivot(
        index="Country",
        columns="Indicator",
        values="Data Coverage (%)"
    )

    fig = px.imshow(
        heatmap_df,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="RdYlGn",
        range_color=[0, 100],
        labels={
            "color": "Coverage (%)",
            "x": "Economic Indicator",
            "y": "Country"
        },
        title="Percentage of Available Annual Observations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # --------------------------------
    # MISSING DATA REPORT
    # --------------------------------

    st.header("Missing Data Report")

    st.write(
        "The following table identifies years for which "
        "the World Bank API did not return an observation."
    )

    missing_only = missing_df[
        missing_df["Missing Years"] != "None"
    ]

    if not missing_only.empty:

        st.dataframe(
            missing_only,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No missing observations were detected "
            "for the selected countries and indicators."
        )

    # --------------------------------
    # INDICATOR-LEVEL SUMMARY
    # --------------------------------

    st.divider()

    st.header("Indicator-Level Data Coverage")

    indicator_summary = (
        quality_df
        .groupby("Indicator")
        .agg({
            "Expected Observations": "sum",
            "Available Observations": "sum",
            "Missing Observations": "sum"
        })
        .reset_index()
    )

    indicator_summary["Coverage (%)"] = (
        indicator_summary["Available Observations"]
        / indicator_summary["Expected Observations"]
        * 100
    )

    st.dataframe(
        indicator_summary.style.format({
            "Coverage (%)": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------
    # DOWNLOAD REPORT
    # --------------------------------

    st.divider()

    st.header("Download Data Quality Report")

    quality_csv = quality_df.to_csv(
        index=False
    ).encode("utf-8")

    missing_csv = missing_df.to_csv(
        index=False
    ).encode("utf-8")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "⬇️ Download Data Coverage Report",
            data=quality_csv,
            file_name="EconScope_Data_Coverage.csv",
            mime="text/csv"
        )

    with col2:

        st.download_button(
            "⬇️ Download Missing Data Report",
            data=missing_csv,
            file_name="EconScope_Missing_Data.csv",
            mime="text/csv"
        )

    # --------------------------------
    # METHODOLOGY AND LIMITATIONS
    # --------------------------------

    with st.expander("Understand the Data Quality Methodology"):

        st.markdown(
            """
            **Data Source:** World Bank Open Data API.

            **Coverage Calculation:**

            Data Coverage (%) =

            Available Observations / Expected Observations × 100

            **Interpretation:**

            - 100% means all expected annual observations were returned.
            - Lower coverage indicates that one or more annual observations
              were unavailable.
            - Missing observations are not automatically treated as zero.

            **Important Limitation:**

            This assessment measures the availability of returned
            annual observations. It does not independently verify
            the accuracy, reliability or comparability of the
            underlying economic estimates.
            """
        )

    st.caption(
        "EconScope | Data Source: World Bank Open Data"
    )