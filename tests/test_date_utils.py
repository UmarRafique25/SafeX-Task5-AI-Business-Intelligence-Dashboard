"""
test_date_utils.py

Tests date filtering and period comparison utilities.
"""

from src.data_loader import load_and_validate

from src.date_utils import (
    get_date_range,
    filter_by_date,
    get_period_length,
    get_previous_period,
    get_comparison_periods,
    get_last_7_days,
    get_last_30_days,
    get_current_month,
    get_previous_month
)


# ============================================================
# LOAD DATA
# ============================================================

FILE_PATH = "data/sample_business_data.csv"

df = load_and_validate(
    FILE_PATH
)


# ============================================================
# AVAILABLE DATE RANGE
# ============================================================

start_date, end_date = get_date_range(
    df
)

print("\n" + "=" * 60)
print("AVAILABLE DATE RANGE")
print("=" * 60)

print(
    f"Start: {start_date.date()}"
)

print(
    f"End:   {end_date.date()}"
)


# ============================================================
# CUSTOM DATE FILTER
# ============================================================

custom_start = "2026-05-01"
custom_end = "2026-05-15"

filtered_df = filter_by_date(
    df,
    custom_start,
    custom_end
)

print("\n" + "=" * 60)
print("CUSTOM DATE FILTER")
print("=" * 60)

print(
    f"Selected: {custom_start} → {custom_end}"
)

print(
    f"Rows: {len(filtered_df)}"
)


# ============================================================
# PERIOD LENGTH
# ============================================================

period_length = get_period_length(
    custom_start,
    custom_end
)

print(
    f"Period length: {period_length} days"
)


# ============================================================
# PREVIOUS PERIOD
# ============================================================

previous_start, previous_end = (
    get_previous_period(
        custom_start,
        custom_end
    )
)

print("\n" + "=" * 60)
print("PREVIOUS PERIOD")
print("=" * 60)

print(
    f"Current:  {custom_start} → {custom_end}"
)

print(
    f"Previous: "
    f"{previous_start.date()} → "
    f"{previous_end.date()}"
)


# ============================================================
# COMPARISON DATASETS
# ============================================================

(
    current_df,
    previous_df,
    comparison_start,
    comparison_end
) = get_comparison_periods(
    df,
    custom_start,
    custom_end
)

print("\n" + "=" * 60)
print("COMPARISON DATA")
print("=" * 60)

print(
    f"Current rows: "
    f"{len(current_df)}"
)

print(
    f"Previous rows: "
    f"{len(previous_df)}"
)


# ============================================================
# LAST 7 DAYS
# ============================================================

last_7 = get_last_7_days(
    df
)

print("\n" + "=" * 60)
print("LAST 7 DAYS")
print("=" * 60)

print(
    f"Rows: {len(last_7)}"
)

print(
    f"Start: "
    f"{last_7['date'].min().date()}"
)

print(
    f"End: "
    f"{last_7['date'].max().date()}"
)


# ============================================================
# LAST 30 DAYS
# ============================================================

last_30 = get_last_30_days(
    df
)

print("\n" + "=" * 60)
print("LAST 30 DAYS")
print("=" * 60)

print(
    f"Rows: {len(last_30)}"
)

print(
    f"Start: "
    f"{last_30['date'].min().date()}"
)

print(
    f"End: "
    f"{last_30['date'].max().date()}"
)


# ============================================================
# CURRENT MONTH
# ============================================================

current_month = get_current_month(
    df
)

print("\n" + "=" * 60)
print("CURRENT MONTH")
print("=" * 60)

print(
    f"Rows: {len(current_month)}"
)

print(
    f"Start: "
    f"{current_month['date'].min().date()}"
)

print(
    f"End: "
    f"{current_month['date'].max().date()}"
)


# ============================================================
# PREVIOUS MONTH
# ============================================================

previous_month = get_previous_month(
    df
)

print("\n" + "=" * 60)
print("PREVIOUS MONTH")
print("=" * 60)

print(
    f"Rows: {len(previous_month)}"
)

print(
    f"Start: "
    f"{previous_month['date'].min().date()}"
)

print(
    f"End: "
    f"{previous_month['date'].max().date()}"
)


print("\n" + "=" * 60)
print("DATE UTILITY TESTS COMPLETED")
print("=" * 60)