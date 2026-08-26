"""
test_metrics.py

Tests the business KPI calculation engine.
"""

from src.data_loader import load_and_validate

from src.metrics import (
    calculate_total_revenue,
    calculate_total_orders,
    calculate_total_traffic,
    calculate_average_order_value,
    calculate_conversion_rate,
    calculate_roas,
    calculate_period_metrics,
    get_kpi_summary
)


# ============================================================
# LOAD DATA
# ============================================================

FILE_PATH = "data/sample_business_data.csv"

df = load_and_validate(
    FILE_PATH
)


# ============================================================
# CALCULATE METRICS
# ============================================================

total_revenue = calculate_total_revenue(df)

total_orders = calculate_total_orders(df)

total_traffic = calculate_total_traffic(df)

aov = calculate_average_order_value(df)

conversion_rate = calculate_conversion_rate(df)

roas = calculate_roas(df)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)

print("BUSINESS KPI TEST")

print("=" * 60)

print(
    f"\nTotal Revenue: ${total_revenue:,.2f}"
)

print(
    f"Total Orders: {total_orders:,}"
)

print(
    f"Website Traffic: {total_traffic:,}"
)

print(
    f"Conversion Rate: {conversion_rate:.2f}%"
)

print(
    f"Average Order Value: ${aov:,.2f}"
)

print(
    f"ROAS: {roas:.2f}x"
)


# ============================================================
# PERIOD METRICS
# ============================================================

print("\n" + "=" * 60)

print("ALL PERIOD METRICS")

print("=" * 60)

metrics = calculate_period_metrics(
    df
)

for name, value in metrics.items():

    print(
        f"{name}: {value}"
    )


# ============================================================
# KPI SUMMARY
# ============================================================

print("\n" + "=" * 60)

print("KPI SUMMARY")

print("=" * 60)

kpis = get_kpi_summary(
    df
)

for name, value in kpis.items():

    print(
        f"{name}: {value}"
    )


print("\n" + "=" * 60)

print("METRICS TEST COMPLETED")

print("=" * 60)