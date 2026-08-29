/start
import streamlit as st
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="IFRS 9 Credit Risk Simulator", page_icon="💳", layout="centered")
st.title("💳 Institutional Credit Risk & ECL Simulator")
st.subheader("Interactive IFRS 9 Baseline Parameter Evaluator")
st.markdown("---")

# --- USER PROFILE INPUTS ---
st.sidebar.header("🔍 Borrower Assessment Metrics")

# Wrapping inputs inside a clean, structured web form
with st.sidebar.form(key="risk_assessment_form"):
    credit_util = st.slider("Revolving Credit Utilization Rate", 0.0, 1.5, 0.35, step=0.01)
    loan_age = st.slider("Account Maturity (Loan Age in Months)", 1, 120, 24)
    region = st.selectbox("Geographical Region", ["Region A", "Region B", "Region C", "Unknown"])
    employment = st.selectbox("Employment Designation", ["Salaried", "Self-Employed", "Unemployed", "NA"])
    
    # 🔘 THE NEW ENTERPRISE SUBMIT BUTTON
    submit_button = st.form_submit_form_button(label="🚀 Calculate Credit Risk Staging")

# --- EXECUTE MATHEMATICAL ENGINE ON SUBMIT ---
if submit_button:
    # --- DATA CLEANING SIMULATION ---
    cleaned_util = max(0.0, min(credit_util, 1.0))

    # --- MATH BACKEND SIMULATION ---
    intercept = -1.5
    w_util = 3.2
    w_age = -0.02

    log_odds = intercept + (w_util * cleaned_util) + (w_age * loan_age)
    probability_of_default = 1 / (1 + np.exp(-log_odds))

    # --- IFRS 9 STAGING LOGIC ---
    if probability_of_default > 0.60 or employment == "Unemployed":
        stage = "Stage 3: Default / Impaired Assets"
        color = "🔴"
    elif probability_of_default > 0.15 or cleaned_util > 0.85:
        stage = "Stage 2: Significant Increase in Credit Risk (SICR)"
        color = "🟡"
    else:
        stage = "Stage 1: Healthy Portfolio Asset"
        color = "🟢"

    # --- RENDER RESULTS DISPLAY ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Estimated Probability of Default (PD)", value=f"{probability_of_default:.2%}")
    with col2:
        st.markdown(f"Asset Allocation Status: \n ### {color} {stage}")
else:
    # Default instruction view before clicking submit
    st.warning("👈 Please adjust the borrower metrics in the sidebar and click 'Calculate Credit Risk Staging' to view the live dashboard output metrics.")

st.markdown("---")
st.info("💡 Technical Note: This web deployment pipeline mirrors the numerical optimization coefficients derived from the baseline SAS macro framework.")


