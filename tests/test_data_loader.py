"""
test_data_loader.py

Tests the business data loading and validation pipeline.
"""

from src.data_loader import (
    load_and_validate,
    get_dataset_summary
)


# ============================================================
# FILE PATH
# ============================================================

FILE_PATH = "data/sample_business_data.csv"

# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_and_validate(
        FILE_PATH
    )

    print("\n" + "=" * 60)
    print("DATA VALIDATION SUCCESSFUL")
    print("=" * 60)

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset summary:")

    summary = get_dataset_summary(df)

    for key, value in summary.items():

        print(
            f"{key}: {value}"
        )

    print("\n" + "=" * 60)
    print("ALL VALIDATION CHECKS PASSED")
    print("=" * 60)


except Exception as error:

    print("\n" + "=" * 60)
    print("DATA VALIDATION FAILED")
    print("=" * 60)

    print(
        f"\nError: {error}"
    )