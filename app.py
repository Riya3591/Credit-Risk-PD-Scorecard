import streamlit as st
import pandas as pd
import numpy as np

# App Title & Configuration
st.set_page_config(layout="wide")
st.title("🏛️ Institutional Credit Risk & ECL Engine")
st.subheader("Automated IFRS 9 Baseline Parameter Evaluator")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Global Risk Parameters")
lgd_input = st.sidebar.slider("Global Loss Given Default (LGD)", 0.1, 1.0, 0.45, help="Percentage loss if default occurs")
pd_cutoff = st.sidebar.slider("Probability of Default (PD) Cutoff", 0.01, 0.50, 0.05, help="High-risk class delimiter threshold")

# Data sourcing container
st.sidebar.markdown("---")
st.sidebar.write("### Data Source")
use_sample = st.sidebar.checkbox("Use Simulated Baseline Portfolio", value=True)
uploaded_file = st.sidebar.file_uploader("Upload Custom Loan Portfolio (CSV)", type=["csv"])

# --- CORE MATH UTILITY FUNCTIONS ---
def generate_base_data(records=2000):
    """Generates an evaluation portfolio matrix mimicking data source variables."""
    np.random.seed(42)
    ead = np.random.exponential(scale=150000, size=records) + 10000
    utilization = np.random.beta(a=2, b=5, size=records)
    delinquency_history = np.random.poisson(lam=0.3, size=records)
    
    # Generate authentic binary target flags (Default vs Active) based on risk factors
    latent_score = -2.5 + (delinquency_history * 1.2) + (utilization * 1.5)
    pd_true = 1 / (1 + np.exp(-latent_score))
    default_flag = np.random.binomial(n=1, p=pd_true)
    
    return pd.DataFrame({
        'AccountID': [f"ACC-{i:05d}" for i in range(records)],
        'Exposure_at_Default': ead,
        'Utilization_Rate': utilization,
        'Historical_Delinquencies': delinquency_history,
        'Actual_Default': default_flag
    })

# --- DATA DISCOVERY SECTION ---
if use_sample:
    df = generate_base_data()
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("💡 Please upload a valid evaluation portfolio CSV file or check 'Use Simulated Baseline Portfolio' in the sidebar to run analysis.")
    st.stop()

# --- INITIALIZE FORM CALCULATION BUTTON ---
with st.form("credit_engine_form"):
    st.write(f"📊 Active Portfolio Records for Processing: {len(df):,} records")
    submit_button = st.form_submit_button(label="🚀 Execute Credit Calculations")

if submit_button:
    st.success("Calculations Processed Successfully!")
    
    # ----------------------------------------------------
    # CALCULATIONS: STEP 1 - LOGISTIC RISK SCORE TRANSFORMATION
    # ----------------------------------------------------
    # Emulate the Logistic Scorecard model coefficients from 1_5_Logistic.sas
    intercept = -2.3
    beta_delinq = 1.1
    beta_util = 1.4
    
    # Direct Log-odds scoring matrix execution
    log_odds = intercept + (df['Historical_Delinquencies'] * beta_delinq) + (df['Utilization_Rate'] * beta_util)
    df['Calculated_PD'] = 1 / (1 + np.exp(-log_odds))
    df['Predicted_High_Risk'] = (df['Calculated_PD'] >= pd_cutoff).astype(int)
    
    # Initialize UI presentation tabs
    tab1, tab2, tab3 = st.tabs(["📊 KS & AUC Performance", "🎯 Calibration Matrix", "💰 Record ECL Analytics"])
    
    # ----------------------------------------------------
    # TAB 1: KS METRICS & AUC EVALUATION FORMULAS
    # ----------------------------------------------------
    with tab1:
        st.header("Kolmogorov-Smirnov (KS) & Area Under Curve (AUC)")
        
        # Sort values to calculate operational distribution limits
        df_sorted = df.sort_values(by='Calculated_PD', ascending=False).reset_index(drop=True)
        total_defaults = df_sorted['Actual_Default'].sum()
        total_non_defaults = len(df_sorted) - total_defaults
        
        # Build evaluation metrics safely via cumulative coordinate arrays
cum_defaults = df_sorted['Actual_Default'].cumsum().values
        cum_non_defaults = (1 - df_sorted['Actual_Default']).cumsum().values
        
        tpr = cum_defaults / total_defaults if total_defaults > 0 else np.zeros_like(cum_defaults)
        fpr = cum_non_defaults / total_non_defaults if total_non_defaults > 0 else np.zeros_like(cum_non_defaults)
        
        # Equation for Max KS Gap Location
        ks_gaps = np.abs(tpr - fpr)
        max_ks_value = np.max(ks_gaps)
        
        # Equation for Riemann Sum Trapezoidal Area Under Curve (AUC)
        auc_score = 0.0
        for i in range(1, len(fpr)):
            auc_score += 0.5 * (fpr[i] - fpr[i-1]) * (tpr[i] + tpr[i-1])
            
        col1, col2 = st.columns(2)
        col1.metric("Calculated AUC Score", f"{auc_score:.4f}")
        col2.metric("Max KS Statistic", f"{max_ks_value:.4f}")
        
        # Native line chart execution
        steps = np.linspace(0, 1, len(fpr))
        chart_df = pd.DataFrame({
            'Index Percentile': steps,
            'True Positive Rate (Cumulative Bads)': tpr,
            'False Positive Rate (Cumulative Goods)': fpr
        })
        st.write("##### Risk Separation Distribution Curves")
        st.line_chart(data=chart_df, x='Index Percentile', y=['True Positive Rate (Cumulative Bads)', 'False Positive Rate (Cumulative Goods)'])

    # ----------------------------------------------------
    # TAB 2: PORTFOLIO RISK RATING CALIBRATION MATRIX
    # ----------------------------------------------------
    with tab2:
        st.header("Risk Rating Band Calibration")
        st.caption("Validates estimated probability bands against actual default parameters.")
        
        # Segment portfolio records into explicit credit score buckets
        df['Risk_Band'] = pd.qcut(df['Calculated_PD'], q=5, labels=['Band 1 (Low Risk)', 'Band 2', 'Band 3', 'Band 4', 'Band 5 (High Risk)'], duplicates='drop')
        
        calibration_df = df.groupby('Risk_Band', observed=False).agg(
            Volume=('AccountID', 'count'),
            Avg_Predicted_PD=('Calculated_PD', 'mean'),
            Actual_Default_Rate=('Actual_Default', 'mean')
        ).reset_index()
        
        st.dataframe(calibration_df.style.format({
            'Volume': '{:,}',
            'Avg_Predicted_PD': '{:.2%}',
            'Actual_Default_Rate': '{:.2%}'
        }))
        
        st.write("##### Volatility Cross-Comparison Chart")
        st.bar_chart(data=calibration_df, x='Risk_Band', y=['Avg_Predicted_PD', 'Actual_Default_Rate'])

    # ----------------------------------------------------
    # TAB 3: INDIVIDUAL IFRS 9 EXPECTED CREDIT LOSS (ECL)
    # ----------------------------------------------------
    with tab3:
        st.header("IFRS 9 Expected Credit Loss (ECL) Calculation Matrix")
        st.write("Calculations are fully simulated on real account vectors using formula: $$ECL = PD \\times LGD \\times EAD$$")
        
        # Apply strict financial parameter array multiplications
        df['Calculated_ECL'] = df['Calculated_PD'] * lgd_input * df['Exposure_at_Default']
        
        # Segment exposures into structural IFRS 9 impairment stages
        def assign_stage(row):
            if row['Calculated_PD'] > 0.15:
                return 'Stage 3 (Impaired)'
            elif row['Calculated_PD'] > pd_cutoff:
                return 'Stage 2 (Significant Increase in Risk)'
            else:
                return 'Stage 1 (Performing)'
                
        df['IFRS9_Stage'] = df.apply(assign_stage, axis=1)
        
        # Display summarized financial results across risk bands
        summary_table = df.groupby('IFRS9_Stage', observed=False).agg(
            Total_Accounts=('AccountID', 'count'),
            Total_EAD=('Exposure_at_Default', 'sum'),
Weighted_Avg_PD=('Calculated_PD', lambda x: np.average(x, weights=df.loc[x.index, 'Exposure_at_Default'])),
            Total_ECL_Provision=('Calculated_ECL', 'sum')
        ).reset_index()
        
        st.dataframe(summary_table.style.format({
            'Total_Accounts': '{:,}',
            'Total_EAD': '${:,.2f}',
            'Weighted_Avg_PD': '{:.2%}',
            'Total_ECL_Provision': '${:,.2f}'
        }))
        
        # Expandable raw calculations ledger view
        with st.expander("🔍 View Raw Record Level Ledger"):
            st.dataframe(df[['AccountID', 'Exposure_at_Default', 'Calculated_PD', 'Calculated_ECL', 'IFRS9_Stage']].head(100).style.format({
                'Exposure_at_Default': '${:,.2f}',
                'Calculated_PD': '{:.4%}',
                'Calculated_ECL': '${:,.2f}'
            }))


