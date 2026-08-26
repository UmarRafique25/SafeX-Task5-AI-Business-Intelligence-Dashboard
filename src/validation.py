"""
validation.py

Data quality and business metric validation utilities
for the AI Business Intelligence Dashboard.
"""

import pandas as pd
import numpy as np

# ============================================================
# REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "date",
    "revenue",
    "orders",
    "traffic",
    "marketing_spend",
    "new_customers",
    "returning_customers",
]


# ============================================================
# VALIDATION RESULT
# ============================================================

def create_validation_result(
    check,
    passed,
    message
):
    """
    Create a standard validation result.
    """

    return {
        "check": check,
        "passed": bool(passed),
        "message": message
    }


# ============================================================
# COLUMN VALIDATION
# ============================================================

def validate_required_columns(df):
    """
    Check that all required business columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        return create_validation_result(
            "Required Columns",
            False,
            (
                "Missing columns: "
                + ", ".join(missing_columns)
            )
        )

    return create_validation_result(
        "Required Columns",
        True,
        "All required columns are present."
    )


# ============================================================
# EMPTY DATA VALIDATION
# ============================================================

def validate_not_empty(df):
    """
    Check that the dataset contains records.
    """

    if df is None:

        return create_validation_result(
            "Dataset Exists",
            False,
            "Dataset is None."
        )

    if df.empty:

        return create_validation_result(
            "Dataset Not Empty",
            False,
            "Dataset contains no records."
        )

    return create_validation_result(
        "Dataset Not Empty",
        True,
        f"Dataset contains {len(df):,} records."
    )


# ============================================================
# DATE VALIDATION
# ============================================================

def validate_dates(df):
    """
    Validate the date column.
    """

    if "date" not in df.columns:

        return create_validation_result(
            "Date Validation",
            False,
            "Date column does not exist."
        )

    dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    invalid_count = dates.isna().sum()

    if invalid_count > 0:

        return create_validation_result(
            "Date Validation",
            False,
            (
                f"{invalid_count:,} invalid "
                "date values found."
            )
        )

    return create_validation_result(
        "Date Validation",
        True,
        "All date values are valid."
    )


# ============================================================
# DUPLICATE VALIDATION
# ============================================================

def validate_duplicates(df):
    """
    Check for completely duplicated records.
    """

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        return create_validation_result(
            "Duplicate Records",
            False,
            (
                f"{duplicate_count:,} "
                "duplicate records found."
            )
        )

    return create_validation_result(
        "Duplicate Records",
        True,
        "No duplicate records found."
    )


# ============================================================
# MISSING VALUE VALIDATION
# ============================================================

def validate_missing_values(df):
    """
    Check required columns for missing values.
    """

    columns = [
        column
        for column in REQUIRED_COLUMNS
        if column in df.columns
    ]

    missing_values = (
        df[columns]
        .isna()
        .sum()
        .sum()
    )

    if missing_values > 0:

        return create_validation_result(
            "Missing Values",
            False,
            (
                f"{missing_values:,} missing "
                "values found in required columns."
            )
        )

    return create_validation_result(
        "Missing Values",
        True,
        "No missing values found in required columns."
    )


# ============================================================
# NEGATIVE VALUE VALIDATION
# ============================================================

def validate_non_negative_values(df):
    """
    Check that business quantity fields are not negative.
    """

    numeric_columns = [
        "revenue",
        "orders",
        "traffic",
        "marketing_spend",
        "new_customers",
        "returning_customers"
    ]

    problems = {}

    for column in numeric_columns:

        if column not in df.columns:
            continue

        negative_count = (
            df[column] < 0
        ).sum()

        if negative_count > 0:

            problems[column] = int(
                negative_count
            )

    if problems:

        details = ", ".join(
            f"{column}: {count}"
            for column, count
            in problems.items()
        )

        return create_validation_result(
            "Non-Negative Values",
            False,
            (
                "Negative values found: "
                + details
            )
        )

    return create_validation_result(
        "Non-Negative Values",
        True,
        "No negative business values found."
    )


# ============================================================
# NUMERIC COLUMN VALIDATION
# ============================================================

def validate_numeric_columns(df):
    """
    Check that business metrics contain numeric data.
    """

    numeric_columns = [
        "revenue",
        "orders",
        "traffic",
        "marketing_spend",
        "new_customers",
        "returning_customers"
    ]

    invalid_columns = []

    for column in numeric_columns:

        if column not in df.columns:
            continue

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):

            invalid_columns.append(
                column
            )

    if invalid_columns:

        return create_validation_result(
            "Numeric Columns",
            False,
            (
                "Non-numeric columns: "
                + ", ".join(invalid_columns)
            )
        )

    return create_validation_result(
        "Numeric Columns",
        True,
        "All business metric columns are numeric."
    )


# ============================================================
# DATE ORDER VALIDATION
# ============================================================

def validate_date_order(df):
    """
    Check that dates are ordered chronologically.
    """

    if "date" not in df.columns:

        return create_validation_result(
            "Date Order",
            False,
            "Date column does not exist."
        )

    dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    if not dates.is_monotonic_increasing:

        return create_validation_result(
            "Date Order",
            False,
            "Dates are not in chronological order."
        )

    return create_validation_result(
        "Date Order",
        True,
        "Dates are correctly ordered."
    )


# ============================================================
# FULL DATA VALIDATION
# ============================================================

def validate_dataset(df):
    """
    Run all data quality checks.
    """

    checks = [
        validate_not_empty(df),
        validate_required_columns(df),
        validate_dates(df),
        validate_duplicates(df),
        validate_missing_values(df),
        validate_non_negative_values(df),
        validate_numeric_columns(df),
        validate_date_order(df)
    ]

    passed = all(
        check["passed"]
        for check in checks
    )

    return {
        "passed": passed,
        "checks": checks
    }

# ============================================================
# FORECAST VALIDATION
# ============================================================

def validate_forecast(
    forecast_df,
    forecast_column="forecast",
    expected_days=30
):
    """
    Validate a forecast dataframe.
    """

    checks = []

    # --------------------------------------------------------
    # DataFrame exists
    # --------------------------------------------------------

    if forecast_df is None:

        return {
            "passed": False,
            "checks": [
                create_validation_result(
                    "Forecast Exists",
                    False,
                    "Forecast dataframe is None."
                )
            ]
        }

    # --------------------------------------------------------
    # Forecast column
    # --------------------------------------------------------

    if forecast_column not in forecast_df.columns:

        return {
            "passed": False,
            "checks": [
                create_validation_result(
                    "Forecast Column",
                    False,
                    (
                        f"Column '{forecast_column}' "
                        "does not exist."
                    )
                )
            ]
        }

    # --------------------------------------------------------
    # Expected number of days
    # --------------------------------------------------------

    checks.append(
        create_validation_result(
            "Forecast Length",
            len(forecast_df) == expected_days,
            (
                f"Forecast contains "
                f"{len(forecast_df)} days. "
                f"Expected {expected_days}."
            )
        )
    )

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    if "date" in forecast_df.columns:

        dates = pd.to_datetime(
            forecast_df["date"],
            errors="coerce"
        )

        checks.append(
            create_validation_result(
                "Forecast Dates",
                dates.notna().all(),
                "All forecast dates are valid."
            )
        )

        checks.append(
            create_validation_result(
                "Forecast Date Uniqueness",
                dates.is_unique,
                "Forecast dates are unique."
            )
        )

        checks.append(
            create_validation_result(
                "Forecast Date Order",
                dates.is_monotonic_increasing,
                "Forecast dates are chronological."
            )
        )

    else:

        checks.append(
            create_validation_result(
                "Forecast Dates",
                False,
                "Forecast date column is missing."
            )
        )

    # --------------------------------------------------------
    # Numeric validation
    # --------------------------------------------------------

    values = forecast_df[
        forecast_column
    ]

    checks.append(
        create_validation_result(
            "Forecast Numeric",
            pd.api.types.is_numeric_dtype(values),
            "Forecast values are numeric."
        )
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    checks.append(
        create_validation_result(
            "Forecast Missing Values",
            values.notna().all(),
            "Forecast contains no missing values."
        )
    )

    # --------------------------------------------------------
    # Infinite values
    # --------------------------------------------------------

    checks.append(
        create_validation_result(
            "Forecast Finite Values",
            np.isfinite(values).all(),
            "Forecast contains only finite values."
        )
    )

    # --------------------------------------------------------
    # Negative values
    # --------------------------------------------------------

    checks.append(
        create_validation_result(
            "Forecast Non-Negative",
            (values >= 0).all(),
            "Forecast contains no negative values."
        )
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    passed = all(
        check["passed"]
        for check in checks
    )

    return {
        "passed": passed,
        "checks": checks
    }