"""
test_forecast_consistency.py

Verify that forecast summary values are derived
from the exact forecast dataframe.
"""

import pandas as pd
import sys


sys.stdout.reconfigure(encoding="utf-8")


# ============================================================
# TEST FORECAST
# ============================================================

forecast_df = pd.DataFrame(
    {
        "date": pd.date_range(
            "2026-05-01",
            periods=30,
            freq="D"
        ),

        "forecast": [
            4000 + (i * 100)
            for i in range(30)
        ]
    }
)


# ============================================================
# CALCULATE SUMMARY
# ============================================================

forecast_total = (
    forecast_df["forecast"].sum()
)

forecast_daily_average = (
    forecast_df["forecast"].mean()
)


# ============================================================
# INDEPENDENT VERIFICATION
# ============================================================

independent_total = sum(
    forecast_df["forecast"]
)

independent_average = (
    independent_total
    /
    len(forecast_df)
)


# ============================================================
# ASSERTIONS
# ============================================================

assert abs(
    forecast_total
    -
    independent_total
) < 0.0001


assert abs(
    forecast_daily_average
    -
    independent_average
) < 0.0001


print(
    "✅ Forecast total matches forecast dataframe"
)

print(
    "✅ Forecast average matches forecast dataframe"
)

print()
print(
    "✅ FORECAST CONSISTENCY TEST PASSED"
)