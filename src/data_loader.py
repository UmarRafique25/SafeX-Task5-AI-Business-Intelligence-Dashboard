"""
data_loader.py

Handles loading, validation, and cleaning of business data
for the AI Business Intelligence Dashboard.
"""

import os
import pandas as pd


# ============================================================
# REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "date",
    "orders",
    "revenue",
    "website_traffic",
    "marketing_spend",
    "new_customers",
    "returning_customers"
]


# ============================================================
# NUMERIC COLUMNS
# ============================================================

NUMERIC_COLUMNS = [
    "orders",
    "revenue",
    "website_traffic",
    "marketing_spend",
    "new_customers",
    "returning_customers"
]


# ============================================================
# LOAD CSV
# ============================================================

def load_csv(file_path):
    """
    Load a CSV file into a Pandas DataFrame.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path)

    except Exception as error:
        raise ValueError(
            f"Unable to read CSV file: {error}"
        )

    return df


# ============================================================
# VALIDATE COLUMNS
# ============================================================

def validate_columns(df):
    """
    Check whether all required columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    return True


# ============================================================
# VALIDATE DATA TYPES
# ============================================================

def validate_data_types(df):
    """
    Convert and validate important data types.
    """

    df = df.copy()

    # Convert date
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    if df["date"].isna().any():

        raise ValueError(
            "Invalid date values detected."
        )

    # Convert numeric columns
    for column in NUMERIC_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if df[column].isna().any():

            raise ValueError(
                f"Invalid numeric values detected "
                f"in column: {column}"
            )

    return df


# ============================================================
# CHECK MISSING VALUES
# ============================================================

def check_missing_values(df):
    """
    Check for missing values.
    """

    missing = df[REQUIRED_COLUMNS].isnull().sum()

    total_missing = missing.sum()

    if total_missing > 0:

        missing_details = (
            missing[missing > 0]
            .to_dict()
        )

        raise ValueError(
            f"Missing values detected: "
            f"{missing_details}"
        )

    return True


# ============================================================
# CHECK DUPLICATES
# ============================================================

def check_duplicates(df):
    """
    Check for duplicate rows.
    """

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        raise ValueError(
            f"{duplicate_count} duplicate rows detected."
        )

    return True


# ============================================================
# CHECK DUPLICATE DATES
# ============================================================

def check_duplicate_dates(df):
    """
    Check whether multiple records exist
    for the same date.
    """

    duplicate_dates = (
        df["date"]
        .duplicated()
        .sum()
    )

    if duplicate_dates > 0:

        raise ValueError(
            f"{duplicate_dates} duplicate dates detected."
        )

    return True


# ============================================================
# CHECK NEGATIVE VALUES
# ============================================================

def check_negative_values(df):
    """
    Check for negative business values.
    """

    negative_columns = {}

    for column in NUMERIC_COLUMNS:

        negative_count = (
            df[column] < 0
        ).sum()

        if negative_count > 0:

            negative_columns[column] = (
                int(negative_count)
            )

    if negative_columns:

        raise ValueError(
            "Negative values detected: "
            + str(negative_columns)
        )

    return True


# ============================================================
# CHECK EMPTY DATASET
# ============================================================

def check_empty_dataset(df):
    """
    Ensure that the dataset contains data.
    """

    if df.empty:

        raise ValueError(
            "The uploaded dataset is empty."
        )

    return True


# ============================================================
# SORT DATA
# ============================================================

def sort_data(df):
    """
    Sort business data chronologically.
    """

    df = df.copy()

    df = df.sort_values(
        by="date"
    ).reset_index(drop=True)

    return df


# ============================================================
# COMPLETE VALIDATION
# ============================================================

def validate_dataset(df):
    """
    Run all validation checks.
    """

    check_empty_dataset(df)

    validate_columns(df)

    df = validate_data_types(df)

    check_missing_values(df)

    check_duplicates(df)

    check_duplicate_dates(df)

    check_negative_values(df)

    df = sort_data(df)

    return df


# ============================================================
# DATASET SUMMARY
# ============================================================

def get_dataset_summary(df):
    """
    Return useful dataset information.
    """

    summary = {

        "rows": len(df),

        "columns": len(df.columns),

        "start_date": (
            df["date"]
            .min()
            .strftime("%Y-%m-%d")
        ),

        "end_date": (
            df["date"]
            .max()
            .strftime("%Y-%m-%d")
        ),

        "missing_values": int(
            df.isnull().sum().sum()
        ),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "total_revenue": round(
            df["revenue"].sum(),
            2
        ),

        "total_orders": int(
            df["orders"].sum()
        ),

        "total_traffic": int(
            df["website_traffic"].sum()
        )
    }

    return summary


# ============================================================
# COMPLETE LOAD + VALIDATE PIPELINE
# ============================================================

def load_and_validate(file_path):
    """
    Load a CSV file and perform complete validation.
    """

    df = load_csv(file_path)

    df = validate_dataset(df)

    return df