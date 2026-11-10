
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS


# Load shared dashboard settings
indicator, start_year, end_year = setup_page()


# Page heading
st.title("Individual Country Analysis")

st.write(
    "Explore the historical performance of an individual "
    "country using World Bank economic indicators."
)


# Country selection
country = st.selectbox(
    "Select a country",
    list(COUNTRIES.keys())
)

country_code = COUNTRIES[country]
indicator_code = INDICATORS[indicator]


# Determine indicator unit
unit = "USD" if indicator == "GDP Per Capita" else "%"


# Retrieve and display data
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

                st.metric(
                    "Change from Previous Observation",
                    f"{change:+.2f}"
                )

            else:

                st.metric("Change", "N/A")


        # Historical trend chart
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

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # Data table
        with st.expander("View Individual Country Data"):

            st.dataframe(
                df,
                use_container_width=True
            )


        # CSV download
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Individual Country Data",
            data=csv,
            file_name=f"{country}_{indicator.replace(' ', '_')}.csv",
            mime="text/csv"
        )
