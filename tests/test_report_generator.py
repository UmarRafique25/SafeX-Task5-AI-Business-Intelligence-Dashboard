"""
test_report_generator.py

Test PDF report generation.
"""

import os
import sys


sys.stdout.reconfigure(encoding="utf-8")

from src.report_generator import (
    generate_pdf_report
)


OUTPUT_PATH = (
    "reports/test_business_report.pdf"
)


# ============================================================
# TEST METRICS
# ============================================================

metrics = {
    "total_revenue": 125000.00,
    "total_orders": 1250,
    "total_traffic": 45000,
    "total_marketing_spend": 15000.00,
    "overall_conversion_rate": 3.8,
    "overall_aov": 100.00,
    "new_customers": 800,
    "returning_customers": 450,
    "returning_customer_share": 36.0
}


# ============================================================
# TEST FORECAST
# ============================================================

model_metadata = {
    "selected_model": "Linear Regression",
    "forecast_days": 30,
    "forecast_total": 132000.00,
    "forecast_daily_average": 4400.00,
    "historical_daily_average": 4166.67,
    "forecast_change_percent": 5.60
}


# ============================================================
# TEST AI REPORT
# ============================================================

ai_report = """
## Executive Summary

Revenue performance remained stable during the analysis period.

## Key Changes

- Revenue reached $125,000.
- The business recorded 1,250 orders.
- Conversion rate was 3.8%.

## Business Insights

The business should continue monitoring conversion and retention.

## Recommended Actions

- Review marketing channel performance.
- Monitor customer retention.
- Track conversion trends.

## Forecast Outlook

The selected model estimates higher average daily revenue.
"""


# ============================================================
# GENERATE
# ============================================================

path = generate_pdf_report(
    OUTPUT_PATH,
    metrics,
    model_metadata,
    ai_report=ai_report,
    report_period="Test Period"
)


# ============================================================
# VALIDATE
# ============================================================

assert os.path.exists(
    path
)

assert os.path.getsize(
    path
) > 1000


print(
    "=" * 60
)

print(
    "PDF generated successfully:"
)

print(
    path
)

print(
    "=" * 60
)

print(
    "✅ PDF REPORT TEST PASSED"
)