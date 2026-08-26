"""
test_forecasting_models.py

Test forecasting model comparison.
"""

from src.data_loader import load_and_validate
from src.forecasting import (
    compare_forecasting_models
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
# COMPARE MODELS
# ============================================================

results = compare_forecasting_models(
    df,
    validation_ratio=0.2,
    window=7
)


comparison = results[
    "comparison"
]

best_model = results[
    "best_model"
]


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 75)
print("FORECASTING MODEL COMPARISON")
print("=" * 75)

print(
    comparison.to_string(
        index=False
    )
)

print()
print("=" * 75)

print(
    f"BEST MODEL: {best_model}"
)

print("=" * 75)


# ============================================================
# VALIDATION
# ============================================================

assert len(comparison) == 2

assert (
    comparison["mae"]
    .notna()
    .all()
)

assert (
    comparison["rmse"]
    .notna()
    .all()
)

assert (
    comparison["r2"]
    .notna()
    .all()
)

assert best_model in [
    "7-Day Moving Average",
    "Linear Regression"
]

print()
print(
    "✅ ALL MODEL COMPARISON TESTS PASSED"
)