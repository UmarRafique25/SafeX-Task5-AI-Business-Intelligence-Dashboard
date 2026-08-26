"""
test_best_forecast.py

Test the complete forecasting pipeline.
"""

from src.data_loader import load_and_validate
from src.forecasting import (
    generate_best_forecast
)
import sys


sys.stdout.reconfigure(encoding="utf-8")


DATA_PATH = "data/sample_business_data.csv"


# ============================================================
# LOAD DATA
# ============================================================

df = load_and_validate(
    DATA_PATH
)


# ============================================================
# GENERATE BEST FORECAST
# ============================================================

results = generate_best_forecast(
    df,
    periods=30,
    validation_ratio=0.2,
    window=7
)


# ============================================================
# EXTRACT RESULTS
# ============================================================

best_model = results[
    "best_model"
]

comparison = results[
    "comparison"
]

forecast = results[
    "forecast"
]

combined = results[
    "combined"
]

summary = results[
    "summary"
]


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 75)
print("FINAL FORECAST PIPELINE")
print("=" * 75)

print(
    f"Selected Model: {best_model}"
)

print()

print("MODEL COMPARISON")
print(
    comparison.to_string(
        index=False
    )
)

print()

print("30-DAY FORECAST")
print(
    forecast.to_string(
        index=False
    )
)

print()

print("FORECAST SUMMARY")

for key, value in summary.items():

    print(
        f"{key}: {value:,.2f}"
    )


# ============================================================
# VALIDATION
# ============================================================

assert best_model in [
    "7-Day Moving Average",
    "Linear Regression"
]

assert len(forecast) == 30

assert (
    forecast["forecast"]
    .notna()
    .all()
)

assert (
    forecast["forecast"] >= 0
).all()

assert len(combined) == (
    len(df) + 30
)

assert (
    summary["total_forecast"] >= 0
)

assert (
    summary["average_daily_forecast"] >= 0
)

print()
print(
    "✅ COMPLETE FORECAST PIPELINE PASSED"
)

# ============================================================
# DATE INTEGRITY
# ============================================================

historical_last_date = (
    df["date"].max()
)

forecast_first_date = (
    forecast["date"].min()
)

assert (
    forecast_first_date
    == historical_last_date
    + __import__("pandas").Timedelta(days=1)
)

assert (
    forecast["date"].is_monotonic_increasing
)

assert (
    forecast["date"].nunique()
    == 30
)