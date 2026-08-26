"""
test_ai_insights.py

Test AI insight generation.
"""

import sys


sys.stdout.reconfigure(encoding="utf-8")

from src.ai_insights import (
    build_business_context,
    build_insight_prompt
)


# ============================================================
# TEST DATA
# ============================================================

metrics = {
    "total_revenue": 125000,
    "total_orders": 1250,
    "total_marketing_spend": 15000,
    "overall_conversion_rate": 3.8,
    "overall_aov": 100.00
}

model_metadata = {
    "selected_model": "Linear Regression",
    "forecast_days": 30,
    "forecast_total": 132000,
    "forecast_daily_average": 4400,
    "historical_daily_average": 4166.67,
    "forecast_change_percent": 5.6
}


# ============================================================
# CONTEXT TEST
# ============================================================

context = build_business_context(
    metrics,
    model_metadata
)

assert (
    context["business_metrics"]
    == metrics
)

assert (
    context["forecast"]
    == model_metadata
)


# ============================================================
# PROMPT TEST
# ============================================================

prompt = build_insight_prompt(
    context
)

assert (
    "125000"
    in prompt
)

assert (
    "Linear Regression"
    in prompt
)

assert (
    "Do not invent"
    in prompt
)


print(
    "✅ AI INSIGHT MODULE TESTS PASSED"
)