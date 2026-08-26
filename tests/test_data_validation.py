"""
test_data_validation.py

Test the data validation module.
"""

import pandas as pd
import sys


sys.stdout.reconfigure(encoding="utf-8")

from src.validation import (
    validate_dataset
)


# ============================================================
# TEST DATA
# ============================================================

df = pd.DataFrame(
    {
        "date": pd.date_range(
            "2026-01-01",
            periods=10,
            freq="D"
        ),

        "revenue": [
            1000,
            1100,
            1200,
            1150,
            1300,
            1400,
            1500,
            1450,
            1600,
            1700
        ],

        "orders": [
            10,
            11,
            12,
            11,
            13,
            14,
            15,
            14,
            16,
            17
        ],

        "traffic": [
            500,
            520,
            550,
            540,
            580,
            600,
            620,
            610,
            650,
            680
        ],

        "marketing_spend": [
            100,
            110,
            120,
            115,
            125,
            130,
            140,
            135,
            145,
            150
        ],

        "new_customers": [
            6,
            7,
            7,
            6,
            8,
            9,
            9,
            8,
            10,
            11
        ],

        "returning_customers": [
            4,
            4,
            5,
            5,
            5,
            5,
            6,
            6,
            6,
            6
        ]
    }
)


# ============================================================
# RUN VALIDATION
# ============================================================

result = validate_dataset(
    df
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

for check in result["checks"]:

    status = (
        "PASS"
        if check["passed"]
        else "FAIL"
    )

    print(
        f"[{status}] "
        f"{check['check']}: "
        f"{check['message']}"
    )


# ============================================================
# ASSERTION
# ============================================================

assert result["passed"] is True

print()
print(
    "✅ DATA VALIDATION TEST PASSED"
)
# ============================================================
# NEGATIVE TEST
# ============================================================

bad_df = pd.read_csv(
    "data/test_bad_data.csv"
)


bad_result = validate_dataset(
    bad_df
)

for check in bad_result["checks"]:

    if (
        check["check"] == "Non-Negative Values"
        and not check["passed"]
    ):

        print(
            f"[FAIL] {check['check']}: "
            f"{check['message']}"
        )

negative_check = next(
    check
    for check in bad_result["checks"]
    if check["check"] == "Non-Negative Values"
)

assert bad_result["passed"] is False
assert negative_check["passed"] is False

print(
    "✅ NEGATIVE DATA TEST PASSED"
)