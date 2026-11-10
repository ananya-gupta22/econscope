
import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

from common import setup_page, COUNTRIES
from data import get_world_bank_data, INDICATORS


# --------------------------------
# PAGE SETUP
# --------------------------------

indicator, start_year, end_year = setup_page()

st.title("📉 Econometric Regression Analysis")

st.write(
    "Examine the relationship between GDP growth, "
    "inflation and unemployment using Ordinary Least Squares."
)


# --------------------------------
# COUNTRY SELECTION
# --------------------------------

country = st.selectbox(
    "Select Country",
    list(COUNTRIES.keys()),
    key="regression_country"
)

country_code = COUNTRIES[country]


# --------------------------------
# DATA COLLECTION
# --------------------------------

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

                temp_df = temp_df[
                    ["Year", "Value"]
                ].copy()

                temp_df["Year"] = pd.to_numeric(
                    temp_df["Year"],
                    errors="coerce"
                )

                temp_df["Value"] = pd.to_numeric(
                    temp_df["Value"],
                    errors="coerce"
                )

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


    # --------------------------------
    # REGRESSION MODEL
    # --------------------------------

    if regression_data is not None:

        regression_data = regression_data.dropna()

        if len(regression_data) >= 8:

            y = regression_data["GDP Growth"]

            X = regression_data[
                ["Inflation", "Unemployment"]
            ]

            X = sm.add_constant(X)

            model = sm.OLS(y, X).fit()


            # --------------------------------
            # REGRESSION RESULTS
            # --------------------------------

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


            # --------------------------------
            # COEFFICIENTS AND P-VALUES
            # --------------------------------

            st.subheader("Regression Coefficients")

            results_df = pd.DataFrame({
                "Coefficient": model.params,
                "P-value": model.pvalues
            })

            st.dataframe(
                results_df.style.format("{:.4f}"),
                use_container_width=True
            )


            # --------------------------------
            # AUTOMATIC ECONOMIC INTERPRETATION
            # --------------------------------

            st.subheader("Economic Interpretation")

            st.write(
                "The following interpretations explain the estimated "
                "relationships in the selected country's regression model."
            )

            for variable in ["Inflation", "Unemployment"]:

                coefficient = model.params[variable]
                p_value = model.pvalues[variable]

                st.markdown(f"**{variable}**")

                if coefficient > 0:
                    direction = "increase"
                elif coefficient < 0:
                    direction = "decrease"
                else:
                    direction = "no estimated change"

                st.write(
                    f"A one-percentage-point increase in {variable.lower()} "
                    f"is associated with an estimated "
                    f"{abs(coefficient):.4f} percentage-point "
                    f"{direction} in GDP growth, holding the other "
                    f"explanatory variable constant."
                )

                if p_value < 0.01:
                    significance = "statistically significant at the 1% level"
                elif p_value < 0.05:
                    significance = "statistically significant at the 5% level"
                elif p_value < 0.10:
                    significance = "statistically significant at the 10% level"
                else:
                    significance = "not statistically significant at the 10% level"

                st.write(
                    f"The coefficient is {significance} "
                    f"(p-value: {p_value:.4f})."
                )

                st.divider()

            # R-squared interpretation

            st.markdown("**Model Explanatory Power**")

            st.write(
                f"The model has an R-squared of {model.rsquared:.3f}. "
                f"This means that approximately "
                f"{model.rsquared * 100:.1f}% of the variation in GDP growth "
                f"in this sample is explained by inflation and unemployment."
            )

            st.caption(
                "Interpretation note: These are conditional statistical "
                "associations, not causal effects. Statistical significance "
                "does not establish economic importance or causality."
            )

            # --------------------------------
            # ACTUAL VS PREDICTED
            # --------------------------------

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
       

            # --------------------------------
            # ECONOMETRIC DIAGNOSTICS
            # --------------------------------

            st.divider()

            st.header("Econometric Diagnostic Tests")

            st.write(
                "Diagnostic tests help assess whether the "
                "regression model satisfies important statistical "
                "assumptions."
            )

            residuals = model.resid
            fitted_values = model.fittedvalues

            # Durbin-Watson
            dw_stat = durbin_watson(residuals)

            # Jarque-Bera
            jb_stat, jb_pvalue, skewness, kurtosis = (
                jarque_bera(residuals)
            )

            # Breusch-Pagan
            bp_stat, bp_pvalue, f_stat, f_pvalue = (
                het_breuschpagan(residuals, X)
            )

            # Variance Inflation Factor
            vif_data = pd.DataFrame()

            vif_data["Variable"] = X.columns

            vif_data["VIF"] = [
                variance_inflation_factor(
                    X.values,
                    i
                )
                for i in range(X.shape[1])
            ]

            vif_data = vif_data[
                vif_data["Variable"] != "const"
            ]


            # --------------------------------
            # DISPLAY TEST RESULTS
            # --------------------------------

            st.subheader("1. Durbin–Watson Test")

            st.metric(
                "Durbin–Watson Statistic",
                f"{dw_stat:.3f}"
            )

            st.caption(
                "Values near 2 suggest little first-order "
                "autocorrelation. Values substantially below 2 "
                "suggest positive autocorrelation; values above 2 "
                "suggest negative autocorrelation."
            )

            st.divider()

            st.subheader("2. Jarque–Bera Test")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "JB Statistic",
                    f"{jb_stat:.3f}"
                )

            with col2:
                st.metric(
                    "P-value",
                    f"{jb_pvalue:.4f}"
                )

            if jb_pvalue < 0.05:
                st.warning(
                    "The null hypothesis of normally distributed "
                    "residuals is rejected at the 5% significance level."
                )
            else:
                st.info(
                    "The null hypothesis of normally distributed "
                    "residuals is not rejected at the 5% significance level."
                )

            st.divider()

            st.subheader("3. Breusch–Pagan Test")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "BP Statistic",
                    f"{bp_stat:.3f}"
                )

            with col2:
                st.metric(
                    "P-value",
                    f"{bp_pvalue:.4f}"
                )

            if bp_pvalue < 0.05:
                st.warning(
                    "Evidence of heteroskedasticity was detected "
                    "at the 5% significance level."
                )
            else:
                st.info(
                    "The null hypothesis of constant error variance "
                    "is not rejected at the 5% significance level."
                )

            st.divider()

            st.subheader("4. Variance Inflation Factor (VIF)")

            st.dataframe(
                vif_data.style.format({
                    "VIF": "{:.3f}"
                }),
                use_container_width=True
            )

            st.caption(
                "VIF measures multicollinearity among explanatory "
                "variables. Values above 5 can indicate a potential "
                "multicollinearity concern; values above 10 indicate "
                "a more serious concern. These are rules of thumb."
            )

            st.divider()

            # --------------------------------
            # RESIDUAL ANALYSIS
            # --------------------------------

            st.subheader("5. Residual Analysis")

            residual_data = pd.DataFrame({
                "Year": regression_data["Year"],
                "Fitted Values": fitted_values,
                "Residuals": residuals
            })

            fig_residuals = px.scatter(
                residual_data,
                x="Fitted Values",
                y="Residuals",
                hover_data=["Year"],
                title="Residuals vs Fitted Values"
            )

            fig_residuals.add_hline(
                y=0,
                line_dash="dash"
            )

            st.plotly_chart(
                fig_residuals,
                use_container_width=True
            )

            fig_residual_time = px.line(
                residual_data,
                x="Year",
                y="Residuals",
                markers=True,
                title="Residuals Over Time"
            )

            fig_residual_time.add_hline(
                y=0,
                line_dash="dash"
            )

            st.plotly_chart(
                fig_residual_time,
                use_container_width=True
            )

            st.caption(
                "Residuals are the differences between actual and "
                "predicted GDP growth. Patterns or systematic changes "
                "may indicate model misspecification."
            )


            # --------------------------------
            # FULL REGRESSION SUMMARY
            # --------------------------------

            with st.expander("View Full Regression Summary"):

                st.text(model.summary().as_text())


            # --------------------------------
            # MODEL EQUATION AND LIMITATIONS
            # --------------------------------

            st.caption(
                "Model: GDP Growth = β0 + β1(Inflation) "
                "+ β2(Unemployment) + ε"
            )

            st.warning(
                "These are exploratory OLS results, not evidence "
                "of causation. The annual sample may be small. "
                "Diagnostic tests also have limited power with "
                "few observations. Time-series properties, omitted "
                "variables and serial correlation can affect estimates."
            )


            # --------------------------------
            # DOWNLOAD DATA
            # --------------------------------

            regression_csv = regression_data.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Regression Dataset",
                data=regression_csv,
                file_name="EconScope_Regression_Data.csv",
                mime="text/csv"
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
