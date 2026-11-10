
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Load shared dashboard settings
indicator, start_year, end_year = setup_page()

# Page heading
st.title("🔍 Economic Relationship Analysis")

st.write(
    "Investigate relationships between economic indicators "
    "across countries using interactive scatter plots."
)

# Available indicators
available_relationship_indicators = [
    name for name in INDICATORS.keys()
    if name in [
        "GDP Growth",
        "GDP Per Capita",
        "Inflation",
        "Unemployment"
    ]
]

# Select indicators
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

# Validate selections
if x_indicator == y_indicator:

    st.warning("Please select two different indicators.")

elif start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    relationship_data = []

    # Retrieve data
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

    # Analyse relationships
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

                # Summary metrics
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

                # Scatter plot with trendline
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

                # Dataset and download
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
