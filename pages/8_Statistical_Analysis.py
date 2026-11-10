
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Shared sidebar settings
indicator, start_year, end_year = setup_page()

st.title("📈 Statistical Analysis")
st.write(
    "Explore descriptive statistics and relationships "
    "between economic indicators."
)

# Select country
country = st.selectbox(
    "Select Country",
    list(COUNTRIES.keys()),
    key="statistics_country"
)

country_code = COUNTRIES[country]

if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    # --------------------------------
    # DESCRIPTIVE STATISTICS
    # --------------------------------

    st.header("Descriptive Statistics")

    st.write(
        f"Statistical summary of {indicator} for {country}."
    )

    with st.spinner("Calculating descriptive statistics..."):

        df = get_world_bank_data(
            country_code,
            INDICATORS[indicator],
            start_year,
            end_year
        )

    if not df.empty:

        values = pd.to_numeric(
            df["Value"],
            errors="coerce"
        ).dropna()

        if not values.empty:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Mean", f"{values.mean():,.2f}")

            with col2:
                st.metric("Median", f"{values.median():,.2f}")

            with col3:
                st.metric(
                    "Standard Deviation",
                    f"{values.std():,.2f}" if len(values) > 1 else "N/A"
                )

            col4, col5 = st.columns(2)

            with col4:
                st.metric("Minimum", f"{values.min():,.2f}")

            with col5:
                st.metric("Maximum", f"{values.max():,.2f}")

            st.caption(
                f"Based on {len(values)} available annual "
                f"observations for {country}."
            )

            with st.expander("View Descriptive Statistics Dataset"):

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

        else:
            st.info("No valid numerical observations are available.")

    else:
        st.info("Statistical analysis will appear when data is available.")

    st.divider()

    # --------------------------------
    # ECONOMIC CORRELATION ANALYSIS
    # --------------------------------

    st.header("🔬 Economic Correlation Analysis")

    st.write(
        "Explore the relationships between different economic "
        "indicators for the selected country."
    )

    correlation_data = None

    with st.spinner("Retrieving indicators for correlation analysis..."):

        for indicator_name, indicator_code in INDICATORS.items():

            indicator_df = get_world_bank_data(
                country_code,
                indicator_code,
                start_year,
                end_year
            )

            if not indicator_df.empty:

                indicator_df = indicator_df[
                    ["Year", "Value"]
                ].copy()

                indicator_df["Year"] = pd.to_numeric(
                    indicator_df["Year"],
                    errors="coerce"
                )

                indicator_df["Value"] = pd.to_numeric(
                    indicator_df["Value"],
                    errors="coerce"
                )

                indicator_df = indicator_df.rename(
                    columns={"Value": indicator_name}
                )

                if correlation_data is None:

                    correlation_data = indicator_df

                else:

                    correlation_data = pd.merge(
                        correlation_data,
                        indicator_df,
                        on="Year",
                        how="outer"
                    )

    if correlation_data is not None:

        correlation_data = correlation_data.sort_values("Year")

        available_indicators = [
            name for name in INDICATORS.keys()
            if name in correlation_data.columns
        ]

        if len(available_indicators) >= 2:

            correlation_matrix = correlation_data[
                available_indicators
            ].corr(
                method="pearson",
                min_periods=3
            )

            if correlation_matrix.notna().any().any():

                correlation_fig = px.imshow(
                    correlation_matrix,
                    text_auto=".2f",
                    color_continuous_scale="RdBu",
                    zmin=-1,
                    zmax=1,
                    aspect="auto",
                    title=f"Economic Correlation Matrix — {country}"
                )

                correlation_fig.update_layout(
                    template="plotly_white",
                    coloraxis_colorbar_title="Correlation"
                )

                st.plotly_chart(
                    correlation_fig,
                    use_container_width=True
                )

                st.subheader("Correlation Results")

                st.dataframe(
                    correlation_matrix.style.format("{:.2f}"),
                    use_container_width=True
                )

                st.caption(
                    "Pearson correlation coefficients are calculated "
                    "using available paired annual observations. "
                    "At least three paired observations are required. "
                    "Correlation does not imply causation."
                )

            else:

                st.warning(
                    "Insufficient overlapping observations "
                    "to calculate correlations."
                )

        else:

            st.warning(
                "At least two economic indicators must have data."
            )

        with st.expander("View Data Used for Correlation Analysis"):

            st.dataframe(
                correlation_data,
                use_container_width=True
            )

    else:

        st.warning(
            "Unable to retrieve sufficient economic data."
        )
