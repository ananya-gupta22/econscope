
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
# PROFESSIONAL UI STYLING
# --------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

/* Main content area */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #111C30;
    border-right: 1px solid #263750;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #60A5FA;
}

/* Main headings */
h1, h2, h3 {
    color: #F8FAFC !important;
}

/* Paragraphs */
p {
    color: #CBD5E1;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #16243A;
    border: 1px solid #263750;
    padding: 18px;
    border-radius: 12px;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #60A5FA;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
}

/* Button hover */
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #1D4ED8;
    color: white;
    border: none;
}

/* Dividers */
hr {
    border-color: #263750;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #263750;
    border-radius: 10px;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #111C30;
    border: 1px solid #263750;
    border-radius: 10px;
}

/* Select boxes */
[data-testid="stSelectbox"] {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

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
st.markdown(
    "### Explore the World Through Economic Data"
)

st.caption(
    "GLOBAL ECONOMIC INTELLIGENCE | WORLD BANK OPEN DATA"
)

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

# Initialise variables
df = pd.DataFrame()

unit = (
    "USD"
    if indicator == "GDP Per Capita"
    else "%"
)

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
# COUNTRY RANKING SYSTEM
# --------------------------------

st.divider()

st.header("🏆 Global Economic Rankings")

st.write(
    "Rank countries according to their economic "
    "indicators and compare their performance."
)

if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

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

        # Download ranking dataset

        ranking_csv = ranking_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Country Rankings",
            data=ranking_csv,
            file_name=f"EconScope_{indicator.replace(' ', '_')}_Rankings_{ranking_year}.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No ranking data available for the selected year."
        )


# --------------------------------
# ECONOMIC PERFORMANCE SCORECARD
# --------------------------------

st.divider()

st.header("🌐 Economic Performance Scorecard")

st.write(
    "A consolidated overview of the selected country's "
    "major macroeconomic indicators."
)

scorecard_indicators = [
    "GDP Growth",
    "GDP Per Capita",
    "Inflation",
    "Unemployment"
]

scorecard_data = {}

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

if start_year >= end_year:

    st.warning("Please select a valid year range.")

elif scorecard_data:

    st.subheader(f"Economic Profile: {country}")

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

                unit = (
                    "$"
                    if name == "GDP Per Capita"
                    else ""
                )

                suffix = (
                    ""
                    if name == "GDP Per Capita"
                    else "%"
                )

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
                        f"{item['Year']}. "
                        f"Delta represents the difference "
                        f"from the previous available observation."
                    )
                )

            else:

                st.metric(
                    label=name,
                    value="N/A"
                )

    st.divider()

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

# --------------------------------
# GLOBAL ECONOMIC MAP
# --------------------------------

st.divider()

st.header("🗺️ Global Economic Map")

st.write(
    "Explore the geographical distribution of the "
    "selected economic indicator across countries."
)

if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    map_data = []

    with st.spinner("Preparing global economic data..."):

        for map_country, map_code in COUNTRIES.items():

            map_df = get_world_bank_data(
                map_code,
                indicator_code,
                start_year,
                end_year
            )

            if not map_df.empty:

                map_df = map_df.dropna(
                    subset=["Value"]
                ).sort_values("Year")

                if not map_df.empty:

                    latest_row = map_df.iloc[-1]

                    map_data.append({
                        "Country": map_country,
                        "ISO3": map_code,
                        "Value": latest_row["Value"],
                        "Year": int(latest_row["Year"])
                    })

    if map_data:

        map_df = pd.DataFrame(map_data)

        map_fig = px.choropleth(
            map_df,
            locations="ISO3",
            color="Value",
            hover_name="Country",
            hover_data={
                "ISO3": False,
                "Value": ":.2f",
                "Year": True
            },
            color_continuous_scale="Blues",
            title=f"Global Distribution of {indicator}",
            labels={
                "Value": indicator
            }
        )

        map_fig.update_layout(
            template="plotly_white",
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type="natural earth"
            ),
            margin=dict(
                l=0,
                r=0,
                t=50,
                b=0
            )
        )

        st.plotly_chart(
            map_fig,
            use_container_width=True
        )

        st.caption(
            "Each country displays its latest available "
            "observation within the selected year range. "
            "Observation years may differ across countries."
        )

        with st.expander("View Global Map Dataset"):

            st.dataframe(
                map_df,
                use_container_width=True,
                hide_index=True
            )

            map_csv = map_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Global Map Data",
                data=map_csv,
                file_name="EconScope_Global_Map_Data.csv",
                mime="text/csv"
            )

    else:

        st.warning(
            "No global data is available for this selection."
        )

 
# --------------------------------
# ECONOMIC RELATIONSHIP ANALYSIS
# --------------------------------

st.divider()

st.header("🔍 Economic Relationship Analysis")

st.write(
    "Investigate relationships between economic indicators "
    "across countries using interactive scatter plots."
)

available_relationship_indicators = [
    name for name in INDICATORS.keys()
    if name in [
        "GDP Growth",
        "GDP Per Capita",
        "Inflation",
        "Unemployment"
    ]
]

col1, col2 = st.columns(2)

with col1:
    x_indicator = st.selectbox(
        "Select X-axis Indicator",
        available_relationship_indicators,
        index=1 if "GDP Per Capita" in available_relationship_indicators else 0,
        key="relationship_x"
    )

with col2:
    y_indicator = st.selectbox(
        "Select Y-axis Indicator",
        available_relationship_indicators,
        index=0,
        key="relationship_y"
    )

if x_indicator == y_indicator:

    st.warning("Please select two different indicators.")

elif start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    relationship_data = []

    with st.spinner("Collecting economic data..."):

        for rel_country, rel_code in COUNTRIES.items():

            x_df = get_world_bank_data(
                rel_code,
                INDICATORS[x_indicator],
                start_year,
                end_year
            )

            y_df = get_world_bank_data(
                rel_code,
                INDICATORS[y_indicator],
                start_year,
                end_year
            )

            if not x_df.empty and not y_df.empty:

                x_df = x_df[["Year", "Value"]].rename(
                    columns={"Value": x_indicator}
                )

                y_df = y_df[["Year", "Value"]].rename(
                    columns={"Value": y_indicator}
                )

                merged = pd.merge(
                    x_df,
                    y_df,
                    on="Year",
                    how="inner"
                )

                merged["Country"] = rel_country

                relationship_data.append(merged)

    if relationship_data:

        relationship_df = pd.concat(
            relationship_data,
            ignore_index=True
        )

        relationship_df = relationship_df.dropna(
            subset=[x_indicator, y_indicator]
        )

        if len(relationship_df) >= 3:

            available_years = sorted(
                relationship_df["Year"].unique()
            )

            selected_relationship_year = st.selectbox(
                "Select Year for Comparison",
                available_years,
                index=len(available_years) - 1,
                key="relationship_year"
            )

            selected_relationship_df = relationship_df[
                relationship_df["Year"] == selected_relationship_year
            ].copy()

            if len(selected_relationship_df) >= 3:

                correlation = selected_relationship_df[
                    [x_indicator, y_indicator]
                ].corr().iloc[0, 1]

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Countries Compared",
                        len(selected_relationship_df)
                    )

                with col2:
                    st.metric(
                        "Pearson Correlation",
                        f"{correlation:.3f}"
                    )

                with col3:
                    if correlation > 0:
                        interpretation = "Positive"
                    elif correlation < 0:
                        interpretation = "Negative"
                    else:
                        interpretation = "No linear relationship"

                    st.metric(
                        "Relationship Direction",
                        interpretation
                    )

                scatter_fig = px.scatter(
                    selected_relationship_df,
                    x=x_indicator,
                    y=y_indicator,
                    color="Country",
                    hover_name="Country",
                    trendline="ols",
                    title=(
                        f"{y_indicator} vs {x_indicator} "
                        f"({selected_relationship_year})"
                    )
                )

                scatter_fig.update_layout(
                    template="plotly_white",
                    xaxis_title=x_indicator,
                    yaxis_title=y_indicator,
                    legend_title="Country"
                )

                st.plotly_chart(
                    scatter_fig,
                    use_container_width=True
                )

                st.caption(
                    "The trendline represents a simple linear "
                    "relationship across the selected countries. "
                    "Correlation does not imply causation."
                )

                with st.expander(
                    "View Economic Relationship Dataset"
                ):

                    st.dataframe(
                        selected_relationship_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    relationship_csv = (
                        selected_relationship_df.to_csv(
                            index=False
                        ).encode("utf-8")
                    )

                    st.download_button(
                        "⬇️ Download Relationship Data",
                        data=relationship_csv,
                        file_name="EconScope_Relationship_Data.csv",
                        mime="text/csv"
                    )

            else:

                st.warning(
                    "Not enough countries have data for both "
                    "indicators in the selected year."
                )

        else:

            st.warning(
                "Insufficient overlapping observations "
                "for relationship analysis."
            )

    else:

        st.warning(
            "Unable to retrieve data for the selected indicators."
        )

# --------------------------------
# ADVANCED COUNTRY COMPARISON
# --------------------------------

st.divider()

st.header("📊 Advanced Country Comparison")

st.write(
    "Compare multiple economic indicators across countries "
    "using standardised values."
)

comparison_indicators = [
    name for name in [
        "GDP Growth",
        "GDP Per Capita",
        "Inflation",
        "Unemployment"
    ]
    if name in INDICATORS
]

advanced_countries = st.multiselect(
    "Select countries",
    options=list(COUNTRIES.keys()),
    default=["India", "Nigeria", "United States"],
    key="advanced_countries"
)

advanced_indicators = st.multiselect(
    "Select economic indicators",
    options=comparison_indicators,
    default=comparison_indicators,
    key="advanced_indicators"
)

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

elif start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    advanced_data = []

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

    if advanced_data:

        advanced_df = pd.DataFrame(advanced_data)

        advanced_pivot = advanced_df.pivot_table(
            index="Country",
            columns="Indicator",
            values="Value",
            aggfunc="first"
        )

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

            st.subheader("Original Economic Values")

            st.dataframe(
                advanced_pivot.style.format("{:,.2f}"),
                use_container_width=True
            )

            with st.expander("View Standardised Comparison Data"):

                st.dataframe(
                    standardised_data.style.format("{:.2f}"),
                    use_container_width=True
                )

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
# TIME-SERIES ANALYSIS
# --------------------------------

st.divider()

st.header("📊 Economic Time-Series Analysis")

st.write(
    "Explore how major economic indicators have changed "
    "over time using annual World Bank data."
)

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

                ts_df = ts_df[["Year", "Value"]].copy()

                ts_df["Year"] = pd.to_numeric(
                    ts_df["Year"], errors="coerce"
                )

                ts_df["Value"] = pd.to_numeric(
                    ts_df["Value"], errors="coerce"
                )

                ts_df = ts_df.dropna()

                time_series_data[indicator_name] = ts_df

if time_series_data:

    st.subheader("Historical Economic Trends")

    for indicator_name, ts_df in time_series_data.items():

        st.markdown(f"### {indicator_name}")

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

    st.subheader("Year-on-Year Changes")

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

    with st.expander("View Complete Time-Series Dataset"):

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

else:

    st.warning(
        "No time-series data is currently available "
        "for the selected country and period."
    )

# --------------------------------
# AUTOMATED ECONOMIC INSIGHTS
# --------------------------------

st.divider()

st.header("💡 Automated Economic Insights")

st.write(
    "Discover important patterns and changes in the "
    "selected country's economic indicators."
)

if time_series_data:

    for indicator_name, ts_df in time_series_data.items():

        insight_df = ts_df[
            ["Year", "Value"]
        ].copy()

        insight_df = insight_df.dropna().sort_values("Year")

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
                f"Insufficient observations for "
                f"{indicator_name}."
            )

    st.caption(
        "Insights are generated using observed annual data. "
        "They describe historical changes and do not establish "
        "causal relationships or predict future outcomes."
    )

else:

    st.warning(
        "Economic insights will appear when data is available."
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

