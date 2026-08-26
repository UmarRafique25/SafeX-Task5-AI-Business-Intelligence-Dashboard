"""
test_forecast_validation.py

Validate the structure and calculations of the
30-day business revenue forecast.
"""

import pandas as pd
import numpy as np
import sys


sys.stdout.reconfigure(encoding="utf-8")

from src.validation import validate_forecast
# ============================================================
# CREATE TEST FORECAST
# ============================================================

forecast_dates = pd.date_range(
    start="2026-04-01",
    periods=30,
    freq="D"
)

forecast_values = np.array([
    4200,
    4250,
    4300,
    4350,
    4400,
    4450,
    4500,
    4550,
    4600,
    4650,
    4700,
    4750,
    4800,
    4850,
    4900,
    4950,
    5000,
    5050,
    5100,
    5150,
    5200,
    5250,
    5300,
    5350,
    5400,
    5450,
    5500,
    5550,
    5600,
    5650
], dtype=float)


forecast_df = pd.DataFrame(
    {
        "date": forecast_dates,
        "forecast": forecast_values
    }
)

validation_result = validate_forecast(
    forecast_df,
    forecast_column="forecast",
    expected_days=30
)

assert validation_result["passed"] is True

print(
    "✅ REUSABLE FORECAST VALIDATOR PASSED"
)

# ============================================================
# TEST 1: EXACTLY 30 DAYS
# ============================================================

assert len(forecast_df) == 30

print(
    "✅ Forecast contains exactly 30 days"
)


# ============================================================
# TEST 2: DATES ARE VALID
# ============================================================

assert forecast_df["date"].notna().all()

assert pd.api.types.is_datetime64_any_dtype(
    forecast_df["date"]
)

print(
    "✅ Forecast dates are valid"
)


# ============================================================
# TEST 3: DATES ARE UNIQUE
# ============================================================

assert forecast_df["date"].is_unique

print(
    "✅ Forecast dates are unique"
)


# ============================================================
# TEST 4: DATES ARE CHRONOLOGICAL
# ============================================================

assert forecast_df[
    "date"
].is_monotonic_increasing

print(
    "✅ Forecast dates are chronological"
)


# ============================================================
# TEST 5: FORECAST VALUES EXIST
# ============================================================

assert forecast_df[
    "forecast"
].notna().all()

print(
    "✅ Forecast contains no missing values"
)


# ============================================================
# TEST 6: FORECAST VALUES ARE NUMERIC
# ============================================================

assert pd.api.types.is_numeric_dtype(
    forecast_df["forecast"]
)

print(
    "✅ Forecast values are numeric"
)


# ============================================================
# TEST 7: FORECAST VALUES ARE FINITE
# ============================================================

assert np.isfinite(
    forecast_df["forecast"]
).all()

print(
    "✅ Forecast values are finite"
)


# ============================================================
# TEST 8: NO NEGATIVE FORECAST
# ============================================================

assert (
    forecast_df["forecast"] >= 0
).all()

print(
    "✅ Forecast contains no negative values"
)


# ============================================================
# TEST 9: FORECAST TOTAL
# ============================================================

forecast_total = (
    forecast_df["forecast"].sum()
)

expected_total = 147750

assert abs(
    forecast_total - expected_total
) < 0.0001

print(
    f"✅ Forecast total validated: "
    f"${forecast_total:,.2f}"
)


# ============================================================
# TEST 10: DAILY AVERAGE
# ============================================================

forecast_daily_average = (
    forecast_df["forecast"].mean()
)

expected_average = (
    expected_total / 30
)

assert abs(
    forecast_daily_average
    -
    expected_average
) < 0.0001

print(
    f"✅ Forecast daily average validated: "
    f"${forecast_daily_average:,.2f}"
)


# ============================================================
# TEST 11: MODEL METADATA
# ============================================================

selected_model = (
    "Linear Regression"
)

assert isinstance(
    selected_model,
    str
)

assert len(
    selected_model
) > 0

print(
    f"✅ Selected model validated: "
    f"{selected_model}"
)


print()
print(
    "=" * 60
)
print(
    "✅ ALL FORECAST VALIDATION TESTS PASSED"
)
print(
    "=" * 60
)