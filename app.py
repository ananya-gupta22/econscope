
import streamlit as st
import pandas as pd
import plotly.express as px

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


st.divider()

st.caption(
    "EconScope | Independent Economics Dashboard Project"
)

st.caption(
    "Source: World Bank Open Data | "
    "Missing observations are excluded from visualisations."
)
