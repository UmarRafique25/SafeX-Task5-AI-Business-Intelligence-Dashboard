"""
metrics.py

Business KPI and performance metrics for the
AI Business Intelligence Dashboard.
"""

import pandas as pd
import numpy as np


# ============================================================
# BASIC KPI CALCULATIONS
# ============================================================

def calculate_total_revenue(df):
    """
    Calculate total business revenue.
    """

    return round(
        df["revenue"].sum(),
        2
    )


def calculate_total_orders(df):
    """
    Calculate total number of orders.
    """

    return int(
        df["orders"].sum()
    )


def calculate_total_traffic(df):
    """
    Calculate total website traffic.
    """

    return int(
        df["website_traffic"].sum()
    )


def calculate_total_marketing_spend(df):
    """
    Calculate total marketing expenditure.
    """

    return round(
        df["marketing_spend"].sum(),
        2
    )


def calculate_total_new_customers(df):
    """
    Calculate total new customers.
    """

    return int(
        df["new_customers"].sum()
    )


def calculate_total_returning_customers(df):
    """
    Calculate total returning customers.
    """

    return int(
        df["returning_customers"].sum()
    )


def calculate_total_customers(df):
    """
    Calculate total customers.
    """

    new_customers = calculate_total_new_customers(df)

    returning_customers = (
        calculate_total_returning_customers(df)
    )

    return (
        new_customers
        + returning_customers
    )


# ============================================================
# CONVERSION RATE
# ============================================================

def calculate_conversion_rate(df):
    """
    Calculate overall website conversion rate.

    Formula:
        Orders / Website Traffic * 100
    """

    total_traffic = calculate_total_traffic(df)

    total_orders = calculate_total_orders(df)

    if total_traffic == 0:
        return 0.0

    conversion_rate = (
        total_orders
        / total_traffic
        * 100
    )

    return round(
        conversion_rate,
        2
    )


# ============================================================
# AVERAGE ORDER VALUE
# ============================================================

def calculate_average_order_value(df):
    """
    Calculate average revenue generated per order.

    Formula:
        Revenue / Orders
    """

    total_orders = calculate_total_orders(df)

    total_revenue = calculate_total_revenue(df)

    if total_orders == 0:
        return 0.0

    aov = (
        total_revenue
        / total_orders
    )

    return round(
        aov,
        2
    )


# ============================================================
# ROAS
# ============================================================

def calculate_roas(df):
    """
    Calculate Return on Ad Spend.

    Formula:
        Revenue / Marketing Spend
    """

    total_revenue = calculate_total_revenue(df)

    total_marketing_spend = (
        calculate_total_marketing_spend(df)
    )

    if total_marketing_spend == 0:
        return 0.0

    roas = (
        total_revenue
        / total_marketing_spend
    )

    return round(
        roas,
        2
    )


# ============================================================
# CUSTOMER MIX
# ============================================================

def calculate_new_customer_ratio(df):
    """
    Calculate percentage of customers
    who are new customers.
    """

    total_customers = calculate_total_customers(df)

    new_customers = (
        calculate_total_new_customers(df)
    )

    if total_customers == 0:
        return 0.0

    ratio = (
        new_customers
        / total_customers
        * 100
    )

    return round(
        ratio,
        2
    )


def calculate_returning_customer_ratio(df):
    """
    Calculate percentage of customers
    who are returning customers.
    """

    total_customers = calculate_total_customers(df)

    returning_customers = (
        calculate_total_returning_customers(df)
    )

    if total_customers == 0:
        return 0.0

    ratio = (
        returning_customers
        / total_customers
        * 100
    )

    return round(
        ratio,
        2
    )


# ============================================================
# DAILY METRICS
# ============================================================

def calculate_daily_metrics(df):
    """
    Create daily business metrics.
    """

    result = df.copy()

    result["conversion_rate"] = np.where(
        result["website_traffic"] > 0,
        (
            result["orders"]
            / result["website_traffic"]
            * 100
        ),
        0
    )

    result["average_order_value"] = np.where(
        result["orders"] > 0,
        (
            result["revenue"]
            / result["orders"]
        ),
        0
    )

    result["roas"] = np.where(
        result["marketing_spend"] > 0,
        (
            result["revenue"]
            / result["marketing_spend"]
        ),
        0
    )

    result["conversion_rate"] = (
        result["conversion_rate"]
        .round(2)
    )

    result["average_order_value"] = (
        result["average_order_value"]
        .round(2)
    )

    result["roas"] = (
        result["roas"]
        .round(2)
    )

    return result


# ============================================================
# PERIOD METRICS
# ============================================================

def calculate_period_metrics(df):
    """
    Calculate all major business KPIs
    for a selected period.
    """

    metrics = {

        "revenue": calculate_total_revenue(df),

        "orders": calculate_total_orders(df),

        "traffic": calculate_total_traffic(df),

        "marketing_spend":
            calculate_total_marketing_spend(df),

        "new_customers":
            calculate_total_new_customers(df),

        "returning_customers":
            calculate_total_returning_customers(df),

        "total_customers":
            calculate_total_customers(df),

        "conversion_rate":
            calculate_conversion_rate(df),

        "average_order_value":
            calculate_average_order_value(df),

        "roas":
            calculate_roas(df),

        "new_customer_ratio":
            calculate_new_customer_ratio(df),

        "returning_customer_ratio":
            calculate_returning_customer_ratio(df)
    }

    return metrics


# ============================================================
# GROWTH CALCULATION
# ============================================================

def calculate_growth(current_value, previous_value):
    """
    Calculate percentage growth between two values.

    Formula:
        ((Current - Previous) / Previous) * 100
    """

    if previous_value == 0:

        if current_value > 0:
            return 100.0

        return 0.0

    growth = (
        (current_value - previous_value)
        / previous_value
        * 100
    )

    return round(
        growth,
        2
    )


# ============================================================
# PERIOD COMPARISON
# ============================================================

def compare_periods(current_df, previous_df):
    """
    Compare current period with previous period.
    """

    current_metrics = (
        calculate_period_metrics(
            current_df
        )
    )

    previous_metrics = (
        calculate_period_metrics(
            previous_df
        )
    )

    comparison = {}

    for metric in current_metrics:

        current_value = (
            current_metrics[metric]
        )

        previous_value = (
            previous_metrics[metric]
        )

        growth = calculate_growth(
            current_value,
            previous_value
        )

        comparison[metric] = {

            "current": current_value,

            "previous": previous_value,

            "growth": growth
        }

    return comparison


# ============================================================
# KPI SUMMARY
# ============================================================

def get_kpi_summary(df):
    """
    Return the main dashboard KPIs.
    """

    metrics = calculate_period_metrics(df)

    return {

        "Total Revenue":
            metrics["revenue"],

        "Total Orders":
            metrics["orders"],

        "Website Traffic":
            metrics["traffic"],

        "Total Customers":
            metrics["total_customers"],

        "Conversion Rate":
            metrics["conversion_rate"],

        "Average Order Value":
            metrics["average_order_value"],

        "ROAS":
            metrics["roas"]
    }

# ============================================================
# DATE-BASED KPI COMPARISON
# ============================================================

def calculate_date_comparison(
    df,
    current_start,
    current_end
):
    """
    Calculate KPI performance for the selected period
    and compare it with the previous equivalent period.
    """

    from src.date_utils import (
        get_comparison_periods
    )

    from src.metrics import (
        compare_periods
    )

    (
        current_df,
        previous_df,
        previous_start,
        previous_end
    ) = get_comparison_periods(
        df,
        current_start,
        current_end
    )

    comparison = compare_periods(
        current_df,
        previous_df
    )

    return {
        "current_df": current_df,
        "previous_df": previous_df,
        "previous_start": previous_start,
        "previous_end": previous_end,
        "comparison": comparison
    }
# ============================================================
# DATE-BASED KPI COMPARISON
# ============================================================
def calculate_date_comparison(
    df,
    current_start,
    current_end
):
    """
    Calculate KPI performance for the selected period
    and compare it with the previous equivalent period.
    """

    from .date_utils import (
        get_comparison_periods
    )

    (
        current_df,
        previous_df,
        previous_start,
        previous_end
    ) = get_comparison_periods(
        df,
        current_start,
        current_end
    )

    comparison = compare_periods(
        current_df,
        previous_df
    )

    return {
        "current_df": current_df,
        "previous_df": previous_df,
        "previous_start": previous_start,
        "previous_end": previous_end,
        "comparison": comparison
    }