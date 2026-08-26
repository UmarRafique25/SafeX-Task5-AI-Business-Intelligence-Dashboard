"""
test_forecasting.py

Tests for the forecasting module.
"""

from src.data_loader import load_and_validate
from src.forecasting import (
    moving_average_forecast,
    forecast_summary,
    create_forecast_dataset
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "data/sample_business_data.csv"

df = load_and_validate(
    DATA_PATH
)


# ============================================================
# GENERATE FORECAST
# ============================================================

forecast = moving_average_forecast(
    df,
    periods=30,
    window=7
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 70)
print("30-DAY REVENUE FORECAST")
print("=" * 70)

print(
    forecast.to_string(
        index=False
    )
)


# ============================================================
# SUMMARY
# ============================================================

summary = forecast_summary(
    forecast
)

print()
print("=" * 70)
print("FORECAST SUMMARY")
print("=" * 70)

for key, value in summary.items():

    print(
        f"{key}: {value:,.2f}"
    )


# ============================================================
# COMBINED DATASET
# ============================================================

combined = create_forecast_dataset(
    df,
    forecast
)

print()
print("=" * 70)
print("COMBINED DATASET")
print("=" * 70)

print(
    combined.tail(40).to_string(
        index=False
    )
)


# ============================================================
# VALIDATION
# ============================================================

assert len(forecast) == 30

assert forecast["forecast"].notna().all()

assert (
    forecast["forecast"] >= 0
).all()

assert (
    forecast["date"].is_monotonic_increasing
)

print()
print("✅ ALL FORECAST TESTS PASSED")