
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Load shared dashboard settings
indicator, start_year, end_year = setup_page()

# Page heading
st.title("🌍 Country Comparison")

st.write(
    "Compare the economic performance of multiple countries "
    "using the same economic indicator."
)

indicator_code = INDICATORS[indicator]

# Select countries
selected_countries = st.multiselect(
    "Select countries to compare",
    options=list(COUNTRIES.keys()),
    default=["India", "Nigeria", "United States"]
)

# Validate selections
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

        # Comparison chart
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
            yaxis_title=indicator,
            hovermode="x unified",
            legend_title="Countries"
        )

        st.plotly_chart(
            comparison_fig,
            use_container_width=True
        )

        # Dataset
        with st.expander("View Country Comparison Dataset"):
            st.dataframe(
                comparison_df,
                use_container_width=True
            )

        # CSV download
        comparison_csv = comparison_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Comparison Data",
            data=comparison_csv,
            file_name="EconScope_Country_Comparison.csv",
            mime="text/csv"
        )

    else:
        st.warning("No data available for the selected countries.")
