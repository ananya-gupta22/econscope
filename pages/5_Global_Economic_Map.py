
import streamlit as st
import pandas as pd
import plotly.express as px

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS

# Load shared dashboard settings
indicator, start_year, end_year = setup_page()

# Page heading
st.title("🗺️ Global Economic Map")

st.write(
    "Explore the geographical distribution of the "
    "selected economic indicator across countries."
)

indicator_code = INDICATORS[indicator]

# Validate year range
if start_year >= end_year:

    st.warning("Please select a valid year range.")

else:

    map_data = []

    # Collect data for all available countries
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

    # Display map
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

        # Dataset and download
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
