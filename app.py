
import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

from data import get_world_bank_data, INDICATORS

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="EconScope | Economics Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# 2. COUNTRY INFORMATION
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
# 3. DASHBOARD HEADER
# --------------------------------

st.title("📊 EconScope")
st.subheader("Explore the World Through Economic Data")

st.write(
    "An interactive platform to explore macroeconomic "
    "indicators and compare economic performance across countries."
)

st.caption("Data Source: World Bank Open Data")

st.divider()

# --------------------------------
# 4. SIDEBAR SETTINGS
# --------------------------------

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

# --------------------------------
# 5. FETCH DATA FOR ONE COUNTRY
# --------------------------------

st.header("Individual Country Analysis")

country = st.selectbox(
    "Select a country for individual analysis",
    list(COUNTRIES.keys())
)

country_code = COUNTRIES[country]
indicator_code = INDICATORS[indicator]

if start_year >= end_year:

    st.error("End year must be later than start year.")

else:

    with st.spinner("Retrieving economic data..."):

        df = get_world_bank_data(
            country_code,
            indicator_code,
            start_year,
            end_year
        )

    if df.empty:

        st.warning("No data available for this selection.")

    else:

        latest = df.iloc[-1]

        col1, col2, col3 = st.columns(3)

        unit = (
            "USD"
            if indicator == "GDP Per Capita"
            else "%"
        )

        with col1:
            value = (
                f"${latest['Value']:,.2f}"
                if unit == "USD"
                else f"{latest['Value']:.2f}%"
            )

            st.metric("Latest Available Value", value)

        with col2:
            st.metric(
                "Latest Available Year",
                int(latest["Year"])
            )

        with col3:
            if len(df) > 1:
                change = latest["Value"] - df.iloc[-2]["Value"]
                st.metric("Change from Previous Observation", f"{change:+.2f}")
            else:
                st.metric("Change", "N/A")

        fig = px.line(
            df,
            x="Year",
            y="Value",
            markers=True,
            title=f"{indicator} in {country}"
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Year",
            yaxis_title=f"{indicator} ({unit})",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("View Individual Country Data"):
            st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Individual Country Data",
            data=csv,
            file_name=f"{country}_{indicator.replace(' ', '_')}.csv",
            mime="text/csv"
        )            

# --------------------------------
# 6. COUNTRY COMPARISON
# --------------------------------

st.divider()

st.header("🌍 Compare Countries")

st.write(
    "Compare the performance of different economies "
    "using the same economic indicator."
)

selected_countries = st.multiselect(
    "Select countries to compare",
    options=list(COUNTRIES.keys()),
    default=["India", "Nigeria", "United States"]
)

if start_year >= end_year:

    st.warning("Please select a valid year range.")

elif len(selected_countries) == 0:

    st.info("Please select at least one country.")

else:

    comparison_data = []

    with st.spinner("Collecting data for selected countries..."):

        for selected_country in selected_countries:

            code = COUNTRIES[selected_country]

            country_data = get_world_bank_data(
                code,
                indicator_code,
                start_year,
                end_year
            )

            if not country_data.empty:

                country_data["Country"] = selected_country

                comparison_data.append(country_data)

    if comparison_data:

        comparison_df = pd.concat(
            comparison_data,
            ignore_index=True
        )

        comparison_fig = px.line(
            comparison_df,
            x="Year",
            y="Value",
            color="Country",
            markers=True,
            title=f"{indicator}: Country Comparison"
        )

        comparison_fig.update_layout(
            template="plotly_white",
            xaxis_title="Year",
            yaxis_title=f"{indicator} ({unit})",
            hovermode="x unified",
            legend_title="Countries"
        )

        st.plotly_chart(
            comparison_fig,
            use_container_width=True
        )


        with st.expander("View Country Comparison Dataset"):
            st.dataframe(
                comparison_df,
                use_container_width=True
            )

        comparison_csv = comparison_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Comparison Data",
            data=comparison_csv,
            file_name="EconScope_Country_Comparison.csv",
            mime="text/csv"
        )
        

# --------------------------------
# 7. STATISTICAL ANALYSIS
# --------------------------------

st.header("📈 Statistical Analysis")

st.write(
    "Explore descriptive statistics for the selected economic data."
)

if not df.empty:

    values = df["Value"]

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
        f"Statistical calculations are based on "
        f"{len(values)} available annual observations "
        f"for {country}."
    )

else:
    st.info(
        "Statistical analysis will appear when economic data is available."
    )

# --------------------------------
# CORRELATION ANALYSIS
# --------------------------------

st.divider()

st.header("🔬 Economic Correlation Analysis")

st.write(
    "Explore the relationships between different economic "
    "indicators for the selected country."
)

if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

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
            ].corr(method="pearson", min_periods=3)

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
                    "At least three paired observations are required."
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


# --------------------------------
# ECONOMETRIC REGRESSION ANALYSIS
# --------------------------------

st.divider()

st.header("📉 Econometric Regression Analysis")

st.write(
    "Explore the relationship between GDP growth, "
    "inflation and unemployment using Ordinary Least Squares."
)

if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    regression_data = None

    regression_indicators = {
        "GDP Growth": INDICATORS["GDP Growth"],
        "Inflation": INDICATORS["Inflation"],
        "Unemployment": INDICATORS["Unemployment"]
    }

    with st.spinner("Preparing regression dataset..."):

        for name, code in regression_indicators.items():

            temp_df = get_world_bank_data(
                country_code,
                code,
                start_year,
                end_year
            )

            if not temp_df.empty:

                temp_df = temp_df.rename(
                    columns={"Value": name}
                )

                if regression_data is None:

                    regression_data = temp_df

                else:

                    regression_data = pd.merge(
                        regression_data,
                        temp_df,
                        on="Year",
                        how="inner"
                    )

    if regression_data is not None:

        regression_data = regression_data.dropna()

        if len(regression_data) >= 8:

            # Dependent variable
            y = regression_data["GDP Growth"]

            # Independent variables
            X = regression_data[
                ["Inflation", "Unemployment"]
            ]

            # Add intercept
            X = sm.add_constant(X)

            # Fit OLS model
            model = sm.OLS(y, X).fit()

            st.subheader("Regression Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "R-squared",
                    f"{model.rsquared:.3f}"
                )

            with col2:
                st.metric(
                    "Adjusted R-squared",
                    f"{model.rsquared_adj:.3f}"
                )

            with col3:
                st.metric(
                    "Observations",
                    int(model.nobs)
                )

            st.subheader("Regression Coefficients")

            results_df = pd.DataFrame({
                "Coefficient": model.params,
                "P-value": model.pvalues
            })

            st.dataframe(
                results_df.style.format("{:.4f}"),
                use_container_width=True
            )

            st.subheader("Actual vs Predicted GDP Growth")

            regression_data = regression_data.copy()

            regression_data["Predicted GDP Growth"] = (
                model.predict(X)
            )

            fig = px.scatter(
                regression_data,
                x="GDP Growth",
                y="Predicted GDP Growth",
                hover_data=["Year"],
                title="Actual vs Predicted GDP Growth",
                labels={
                    "GDP Growth": "Actual GDP Growth (%)",
                    "Predicted GDP Growth": "Predicted GDP Growth (%)"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            with st.expander("View Full Regression Summary"):

                st.text(model.summary().as_text())

            st.caption(
                "Model: GDP Growth = β0 + β1(Inflation) "
                "+ β2(Unemployment) + ε"
            )

            st.warning(
                "Exploratory OLS results are not evidence of causation. "
                "The annual sample may be small, and time-series "
                "properties, omitted variables and serial correlation "
                "can affect the estimates. Further econometric testing "
                "is required before drawing conclusions."
            )

        else:

            st.warning(
                "Insufficient overlapping annual observations. "
                "At least 8 complete observations are required."
            )

    else:

        st.warning(
            "Unable to retrieve the data required for regression."
        )


# --------------------------------
# 8. FOOTER
# --------------------------------

st.divider()

st.caption(
    "EconScope | Independent Economics Dashboard Project"
)

st.caption(
    "Source: World Bank Open Data | "
    "Missing observations are excluded from visualisations."
)

