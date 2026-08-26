"""
test_kpi_comparison.py

Tests KPI comparison functionality.
"""

from src.data_loader import (
    load_and_validate
)

from src.metrics import (
    calculate_date_comparison
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_and_validate(
    "data/sample_business_data.csv"
)


# ============================================================
# SELECT PERIOD
# ============================================================

current_start = "2026-06-01"

current_end = "2026-06-30"


# ============================================================
# CALCULATE COMPARISON
# ============================================================

result = calculate_date_comparison(
    df,
    current_start,
    current_end
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)

print("KPI PERIOD COMPARISON")

print("=" * 70)

print(
    f"\nCurrent Period: "
    f"{current_start} → {current_end}"
)

print(
    f"Previous Period: "
    f"{result['previous_start'].date()} → "
    f"{result['previous_end'].date()}"
)

print("\n" + "-" * 70)

print(
    f"{'Metric':<25}"
    f"{'Current':>15}"
    f"{'Previous':>15}"
    f"{'Growth':>15}"
)

print("-" * 70)


for metric, values in result[
    "comparison"
].items():

    print(
        f"{metric:<25}"
        f"{values['current']:>15}"
        f"{values['previous']:>15}"
        f"{values['growth']:>14.2f}%"
    )


print("=" * 70)