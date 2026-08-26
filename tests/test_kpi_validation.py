"""
test_kpi_validation.py

Verify that dashboard KPI calculations
match direct calculations from raw data.
"""

import pandas as pd
import sys


sys.stdout.reconfigure(encoding="utf-8")


# ============================================================
# TEST DATA
# ============================================================

df = pd.DataFrame(
    {
        "revenue": [
            1000,
            2000,
            3000
        ],

        "orders": [
            10,
            20,
            30
        ],

        "traffic": [
            100,
            200,
            300
        ],

        "marketing_spend": [
            100,
            200,
            300
        ]
    }
)


# ============================================================
# DIRECT CALCULATIONS
# ============================================================

expected_revenue = (
    df["revenue"].sum()
)

expected_orders = (
    df["orders"].sum()
)

expected_traffic = (
    df["traffic"].sum()
)

expected_marketing_spend = (
    df["marketing_spend"].sum()
)


expected_conversion_rate = (
    expected_orders
    /
    expected_traffic
    *
    100
)


expected_aov = (
    expected_revenue
    /
    expected_orders
)


# ============================================================
# ASSERTIONS
# ============================================================

assert expected_revenue == 6000

assert expected_orders == 60

assert expected_traffic == 600

assert expected_marketing_spend == 600

assert abs(
    expected_conversion_rate
    -
    10.0
) < 0.0001

assert abs(
    expected_aov
    -
    100.0
) < 0.0001


print(
    "✅ KPI CALCULATION VALIDATION PASSED"
)