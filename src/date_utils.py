"""
date_utils.py

Date filtering and period comparison utilities
for the AI Business Intelligence Dashboard.
"""

import pandas as pd


# ============================================================
# DATE RANGE
# ============================================================

def get_date_range(df):
    """
    Return the minimum and maximum dates
    available in the dataset.
    """

    start_date = df["date"].min()

    end_date = df["date"].max()

    return start_date, end_date


# ============================================================
# FILTER BY DATE
# ============================================================

def filter_by_date(
    df,
    start_date,
    end_date
):
    """
    Filter the dataset between two dates.

    Both start and end dates are inclusive.
    """

    start_date = pd.to_datetime(
        start_date
    )

    end_date = pd.to_datetime(
        end_date
    )

    filtered_df = df[
        (df["date"] >= start_date)
        &
        (df["date"] <= end_date)
    ].copy()

    return filtered_df


# ============================================================
# PERIOD LENGTH
# ============================================================

def get_period_length(
    start_date,
    end_date
):
    """
    Calculate number of days in a period.
    """

    start_date = pd.to_datetime(
        start_date
    )

    end_date = pd.to_datetime(
        end_date
    )

    return (
        end_date - start_date
    ).days + 1


# ============================================================
# PREVIOUS PERIOD
# ============================================================

def get_previous_period(
    start_date,
    end_date
):
    """
    Calculate the immediately preceding period
    with the same number of days.
    """

    start_date = pd.to_datetime(
        start_date
    )

    end_date = pd.to_datetime(
        end_date
    )

    period_length = get_period_length(
        start_date,
        end_date
    )

    previous_end = (
        start_date
        - pd.Timedelta(days=1)
    )

    previous_start = (
        previous_end
        - pd.Timedelta(
            days=period_length - 1
        )
    )

    return previous_start, previous_end


# ============================================================
# CURRENT + PREVIOUS DATA
# ============================================================

def get_comparison_periods(
    df,
    start_date,
    end_date
):
    """
    Return current and previous period DataFrames.
    """

    current_df = filter_by_date(
        df,
        start_date,
        end_date
    )

    previous_start, previous_end = (
        get_previous_period(
            start_date,
            end_date
        )
    )

    previous_df = filter_by_date(
        df,
        previous_start,
        previous_end
    )

    return (
        current_df,
        previous_df,
        previous_start,
        previous_end
    )


# ============================================================
# PREDEFINED PERIODS
# ============================================================

def get_last_n_days(
    df,
    days
):
    """
    Return the most recent N days available
    in the dataset.
    """

    max_date = df["date"].max()

    start_date = (
        max_date
        - pd.Timedelta(
            days=days - 1
        )
    )

    return filter_by_date(
        df,
        start_date,
        max_date
    )


# ============================================================
# LAST 7 DAYS
# ============================================================

def get_last_7_days(df):
    """
    Return the latest 7 days.
    """

    return get_last_n_days(
        df,
        7
    )


# ============================================================
# LAST 30 DAYS
# ============================================================

def get_last_30_days(df):
    """
    Return the latest 30 days.
    """

    return get_last_n_days(
        df,
        30
    )


# ============================================================
# CURRENT MONTH
# ============================================================

def get_current_month(df):
    """
    Return the month containing the latest
    date available in the dataset.
    """

    max_date = df["date"].max()

    start_date = max_date.replace(
        day=1
    )

    return filter_by_date(
        df,
        start_date,
        max_date
    )


# ============================================================
# PREVIOUS MONTH
# ============================================================

def get_previous_month(df):
    """
    Return the complete month immediately
    before the latest available month.
    """

    max_date = df["date"].max()

    current_month_start = max_date.replace(
        day=1
    )

    previous_month_end = (
        current_month_start
        - pd.Timedelta(days=1)
    )

    previous_month_start = (
        previous_month_end
        .replace(day=1)
    )

    return filter_by_date(
        df,
        previous_month_start,
        previous_month_end
    )