# Problems Encountered & Solutions

## 1. Missing Date Utility Module

### Problem
The KPI date comparison functionality initially produced a `ModuleNotFoundError` because the date utility module was not correctly available to the metrics module.

### Solution
The project structure and import configuration were corrected so that the date utility functions could be accessed correctly.

---

## 2. PDF Generation Failure on Deployment

### Problem
PDF report generation worked differently between the local environment and Streamlit deployment. The deployed application reported that Kaleido required Google Chrome.

### Solution
The deployment environment was updated with the required browser dependency through `packages.txt`, and Kaleido was included in the Python dependencies.

---

## 3. AI Insights Not Available on Initial Deployment

### Problem
AI-generated insights worked locally but were unavailable on the deployed application because the local API key stored in `.env` was not available in the cloud environment.

### Solution
The API key was configured securely through the deployment platform's secrets configuration instead of uploading credentials to GitHub.

---

## 4. Data Validation

### Problem
Business dashboards can produce misleading results when missing, duplicated, invalid, or incorrectly formatted data is processed.

### Solution
Validation checks were implemented before KPI calculations and forecasting to ensure that the analytical pipeline operates on valid data.

---

## 5. Forecast Validation

### Problem
Forecast outputs need to be checked before being presented as business predictions.

### Solution
The forecasting pipeline validates the forecast dates, number of prediction periods, numeric values, missing values, and invalid outputs before displaying results.