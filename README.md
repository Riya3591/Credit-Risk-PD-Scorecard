/start
# Credit Risk Probability of Default (PD) Modeling Pipeline (IFRS 9 Framework)

This repository contains a complete, end-to-end Credit Risk Model Development Lifecycle built using SAS. The pipeline ingests raw historical loan data, executes data quality checks, transforms variables, trains a predictive Logistic Regression model, and validates performance using regulatory-standard metrics.

The project is structured to meet structural and data processing requirements aligned with the IFRS 9 (International Financial Reporting Standards) framework for estimating Expected Credit Losses (ECL).

---

## 🛠️ Project Architecture & Pipeline Workflow

The development is modularized across eight sequential SAS scripts:

1. **1_1_LoadData.sas (Data Ingestion & Cleaning):** Ingests raw historical portfolio metrics (.csv), executes initial data cleansing rules (removing chronologically impossible loan records), caps outliers, and normalizes null values.
2. **1_2_DQ.sas (Data Quality Analysis):** Conducts thorough data diagnostics, auditing missing percentages and verifying statistical distributions.
3. **1_3_DataSplit.sas (Partitioning):** Segregates clean data intoTraining (70%) Testing (30%)** sets to prevent model overfitting.
4. **1_4_FeatureEng.sas (Feature Engineering):** Generates optimized predictive indicators, handles variable binning, and structures borrower risk profiles.
5. **1_5_Logistic.sas (Model Estimation):** Logistic  Regression** classifier to assign Point-in-Time (PIT) Probability of Default (PD) ratings.
6. **1_6_KS&AUC.sas (Model Validation):** Evaluates the model's discriminatory power on oKolmogorov-Smirnov Area Under the ROC Curve (AUC)er the ROC Curve (AUC)** metrics.
7. **1_7_Calibration.sas (Risk Calibration & Macro Overlay):** Calibrates statistical risk scores against historical central tendencies and overlays macroeconomic scenarios (e.g., base, optimistic, adverse) to adjust for forward-looking economic shifts.
8. **1_8_ECL.sas (Expected Credit Loss Engine):** Integrates PD outputs with Exposure at Default (EAD) and Loss Given Default (LGD) metrics to compute final financial provisions under the strict IFRS 9 impairment guidelines.

---

## 📊 Core Features Analyzed

The predictive model assesses credit risk using multi-dimCredit Utilization Rate::
* **Credit Utilization Rate:** Evaluates revolving credit reliance (Loan Maturity (loan_age_m): **Loan Maturity (loan_age_m):** Calculates exact account longevity in months relative Socio-Demographic Indicators:*Socio-Demographic Indicators:** Incorporates regional groupings, employment designations, marital status, and dependent tracking to isolate risk segments.

---

## 🚀 TechLanguage:ments & Toolkit

* **Language:** SAS (SAS Studio Statistical Techniques:s)
* **Statistical Techniques:** Logistic Regression, Binary Classification, Missing Value Imputation.
* **Validation Metrics:** ROC-AUC Curve, KS Statistic, Metadata Structure Auditing (PROC CONTENTS).

---

## 🎓 Credits & Course Reference
This project framework was developed as part of a guided credit risk analytics curriculum on Udemy. Special thanks to the instructor for the architectural design guidance on IFRS 9 risk parameter implementations.

---

## 🛑 Data Disclaimer
Due to data privacy regulations and banking confidentiality agreements, the underlying raw historical dataset (ifrs9_pit_pd_intro.csv) is excluded from this public repository. This repository hosts only the structural source code and model architecture frameworks.


