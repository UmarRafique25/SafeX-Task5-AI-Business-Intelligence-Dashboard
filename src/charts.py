"""
charts.py

Interactive Plotly charts for the
AI Business Intelligence Dashboard.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ============================================================
# REVENUE TREND
# ============================================================

def revenue_trend_chart(df):
    """
    Create an interactive daily revenue trend chart.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["revenue"],
            mode="lines+markers",
            name="Revenue",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Revenue: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Daily Revenue Trend",
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# REVENUE MOVING AVERAGE
# ============================================================

def revenue_moving_average_chart(
    df,
    window=7
):
    """
    Create revenue trend with moving average.
    """

    data = df.copy()

    data["moving_average"] = (
        data["revenue"]
        .rolling(
            window=window,
            min_periods=1
        )
        .mean()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["revenue"],
            mode="lines",
            name="Daily Revenue",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Revenue: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["moving_average"],
            mode="lines",
            name=f"{window}-Day Moving Average",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Moving Average: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Revenue Trend & Moving Average",
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# ORDERS TREND
# ============================================================

def orders_trend_chart(df):
    """
    Create daily orders trend chart.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["orders"],
            name="Orders",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Orders: %{y:,}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Daily Orders",
        xaxis_title="Date",
        yaxis_title="Orders",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# REVENUE VS ORDERS
# ============================================================

def revenue_orders_chart(df):
    """
    Compare revenue and orders over time
    using two Y axes.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["revenue"],
            mode="lines",
            name="Revenue",
            yaxis="y"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["orders"],
            mode="lines",
            name="Orders",
            yaxis="y2"
        )
    )

    fig.update_layout(
        title="Revenue vs Orders",
        xaxis_title="Date",
        yaxis=dict(
            title="Revenue ($)"
        ),
        yaxis2=dict(
            title="Orders",
            overlaying="y",
            side="right"
        ),
        hovermode="x unified",
        template="plotly_white",
        height=450
    )

    return fig


# ============================================================
# DAILY REVENUE DISTRIBUTION
# ============================================================

def revenue_distribution_chart(df):
    """
    Display revenue distribution.
    """

    fig = px.histogram(
        df,
        x="revenue",
        nbins=20,
        title="Revenue Distribution"
    )

    fig.update_layout(
        xaxis_title="Daily Revenue ($)",
        yaxis_title="Number of Days",
        template="plotly_white",
        height=400
    )

    return fig


# ============================================================
# WEEKLY REVENUE
# ============================================================

def weekly_revenue_chart(df):
    """
    Aggregate revenue by week.
    """

    data = df.copy()

    data["week"] = (
        data["date"]
        .dt.to_period("W")
        .apply(lambda x: x.start_time)
    )

    weekly = (
        data
        .groupby("week", as_index=False)
        ["revenue"]
        .sum()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=weekly["week"],
            y=weekly["revenue"],
            name="Weekly Revenue",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Revenue: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Weekly Revenue",
        xaxis_title="Week",
        yaxis_title="Revenue ($)",
        template="plotly_white",
        height=420
    )

    return fig

# ============================================================
# CUSTOMER TREND
# ============================================================

def customer_trend_chart(df):
    """
    Display total customers over time.
    """

    fig = go.Figure()

    total_customers = (
        df["new_customers"]
        + df["returning_customers"]
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=total_customers,
            mode="lines+markers",
            name="Total Customers",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Customers: %{y:,}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Customer Trend",
        xaxis_title="Date",
        yaxis_title="Customers",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# NEW VS RETURNING CUSTOMERS
# ============================================================

def customer_mix_chart(df):
    """
    Compare new and returning customers.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["new_customers"],
            name="New Customers",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "New Customers: %{y:,}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["returning_customers"],
            name="Returning Customers",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Returning Customers: %{y:,}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="New vs Returning Customers",
        xaxis_title="Date",
        yaxis_title="Customers",
        barmode="stack",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# CONVERSION RATE TREND
# ============================================================

def conversion_rate_chart(df):
    """
    Display conversion rate over time.
    """

    fig = go.Figure()

    conversion_rate = (
        df["orders"]
        / df["website_traffic"].replace(0, float("nan"))
        * 100
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=conversion_rate,
            mode="lines+markers",
            name="Conversion Rate",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Conversion Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Conversion Rate Trend",
        xaxis_title="Date",
        yaxis_title="Conversion Rate (%)",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# TRAFFIC VS ORDERS
# ============================================================

def traffic_vs_orders_chart(df):
    """
    Compare website traffic with orders.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["website_traffic"],
            mode="lines",
            name="Website Traffic",
            yaxis="y"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["orders"],
            mode="lines",
            name="Orders",
            yaxis="y2"
        )
    )

    fig.update_layout(
        title="Website Traffic vs Orders",
        xaxis_title="Date",
        yaxis=dict(
            title="Website Traffic"
        ),
        yaxis2=dict(
            title="Orders",
            overlaying="y",
            side="right"
        ),
        hovermode="x unified",
        template="plotly_white",
        height=450
    )

    return fig


# ============================================================
# AVERAGE ORDER VALUE TREND
# ============================================================

def aov_trend_chart(df):
    """
    Display Average Order Value over time.
    """

    data = df.copy()

    data["aov"] = (
        data["revenue"] /
        data["orders"].replace(0, float("nan"))
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["aov"],
            mode="lines+markers",
            name="Average Order Value",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "AOV: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Average Order Value Trend",
        xaxis_title="Date",
        yaxis_title="AOV ($)",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig

# ============================================================
# FORECAST CHART
# ============================================================

def forecast_chart(
    combined_df
):
    """
    Display historical actual revenue and
    future forecast revenue.
    """

    fig = go.Figure()

    historical = combined_df[
        combined_df["actual"].notna()
    ]

    forecast = combined_df[
        combined_df["forecast"].notna()
    ]

    fig.add_trace(
        go.Scatter(
            x=historical["date"],
            y=historical["actual"],
            mode="lines",
            name="Actual Revenue",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Actual: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["date"],
            y=forecast["forecast"],
            mode="lines+markers",
            name="30-Day Forecast",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Forecast: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Revenue Forecast: Next 30 Days",
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )

    return fig

# ============================================================
# MODEL VALIDATION CHART
# ============================================================

def model_validation_chart(
    validation_df,
    model_name
):
    """
    Compare actual and predicted revenue
    during the validation period.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=validation_df["date"],
            y=validation_df["revenue"],
            mode="lines+markers",
            name="Actual Revenue",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Actual: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=validation_df["date"],
            y=validation_df["prediction"],
            mode="lines+markers",
            name=f"{model_name} Prediction",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Prediction: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=(
            f"Validation: Actual vs {model_name}"
        ),
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        hovermode="x unified",
        template="plotly_white",
        height=450
    )

    return fig

