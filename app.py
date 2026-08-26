"""
app.py

Main Streamlit application for the
AI Business Intelligence Dashboard.
"""

import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src"
)

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

import tempfile
import os

from google import genai

from data_loader import (
    load_and_validate
)

from metrics import (
    calculate_period_metrics
)

from datetime import datetime

from report_generator import (
    generate_pdf_report
)

from date_utils import (
    filter_by_date,
    get_date_range,
    get_previous_period
)

from forecasting import (
    generate_best_forecast,
    compare_forecasting_models
)

from ai_insights import (
    generate_business_insights
)

from charts import (
    revenue_trend_chart,
    revenue_moving_average_chart,
    orders_trend_chart,
    revenue_orders_chart,
    revenue_distribution_chart,
    weekly_revenue_chart,
    customer_trend_chart,
    customer_mix_chart,
    conversion_rate_chart,
    traffic_vs_orders_chart,
    aov_trend_chart,
    forecast_chart,
    model_validation_chart
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def prepare_ai_report_for_display(report):
    """
    Escape currency markers so Streamlit does not parse them as math.
    """

    if not report:
        return report

    return report.replace(
        "$",
        r"\$"
    )


def create_report_file(
    metrics,
    model_metadata,
    ai_report,
    revenue_chart=None,
    marketing_chart=None,
    customer_chart=None,
    forecast_chart=None
):
    """
    Generate a temporary PDF report and
    return its path.
    """

    temporary_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    temporary_file.close()

    generate_pdf_report(
        output_path=temporary_file.name,
        metrics=metrics,
        model_metadata=model_metadata,
        ai_report=ai_report,
        revenue_chart=revenue_chart,
        marketing_chart=marketing_chart,
        customer_chart=customer_chart,
        forecast_chart=forecast_chart,
        report_period="Selected Analysis Period"
    )

    return temporary_file.name

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "sample_business_data.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_default_data():

    return load_and_validate(
        DEFAULT_DATA_PATH
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📊 AI Business Intelligence Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Turn business data into clear performance insights, '
    'forecasts, and actionable recommendations.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Dashboard Controls")

    st.subheader("Business Data")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"],
        help=(
            "Upload business data using the required "
            "dataset structure."
        )
    )


# ============================================================
# DATA LOADING
# ============================================================

try:
    if uploaded_file is not None:

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_file
            )
        elif file_name.endswith(".xlsx"):

            df = pd.read_excel(
                uploaded_file
            )

        else:

            st.error(
                "Unsupported file format."
            )

            st.stop()

        # Validate uploaded data
        from data_loader import validate_dataset

        df = validate_dataset(
            df
        )

        data_source = (
            f"Uploaded: {uploaded_file.name}"
        )

    else:

        df = load_default_data()

        data_source = "Sample E-Commerce Dataset"


except Exception as error:

    st.error(
        "Unable to load the business data."
    )

    st.error(
        str(error)
    )

    st.stop()


# ============================================================
# DATA STATUS
# ============================================================

with st.sidebar:

    st.success(
        "✅ Data loaded successfully"
    )

    st.caption(
        data_source
    )

    st.metric(
        "Records",
        f"{len(df):,}"
    )

    st.metric(
        "Columns",
        f"{len(df.columns):,}"
    )


# ============================================================
# DATE RANGE
# ============================================================

min_date, max_date = get_date_range(
    df
)

with st.sidebar:

    st.subheader("📅 Date Range")

    selected_dates = st.date_input(
        "Select analysis period",
        value=(
            min_date.date(),
            max_date.date()
        ),
        min_value=min_date.date(),
        max_value=max_date.date()
    )


# ============================================================
# HANDLE DATE SELECTION
# ============================================================

if isinstance(
    selected_dates,
    tuple
) and len(selected_dates) == 2:

    selected_start = pd.to_datetime(
        selected_dates[0]
    )

    selected_end = pd.to_datetime(
        selected_dates[1]
    )

else:

    selected_start = min_date

    selected_end = max_date


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = filter_by_date(
    df,
    selected_start,
    selected_end
)


# ============================================================
# VALIDATE SELECTED PERIOD
# ============================================================

if filtered_df.empty:

    st.warning(
        "No data exists for the selected date range."
    )

    st.stop()


# ============================================================
# DASHBOARD INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📌 Business Overview'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Analysis period: "
    f"{selected_start.strftime('%d %b %Y')} "
    f"to "
    f"{selected_end.strftime('%d %b %Y')}"
)


# ============================================================
# CALCULATE KPIs
# ============================================================

metrics = calculate_period_metrics(
    filtered_df
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Revenue",
        f"${metrics['revenue']:,.0f}"
    )


with col2:

    st.metric(
        "🛒 Orders",
        f"{metrics['orders']:,}"
    )


with col3:

    st.metric(
        "👥 Customers",
        f"{metrics['total_customers']:,}"
    )


with col4:

    st.metric(
        "📈 Conversion Rate",
        f"{metrics['conversion_rate']:.2f}%"
    )


# ============================================================
# SECOND KPI ROW
# ============================================================

col5, col6, col7, col8 = st.columns(4)


with col5:

    st.metric(
        "🌐 Website Traffic",
        f"{metrics['traffic']:,}"
    )


with col6:

    st.metric(
        "💵 Average Order Value",
        f"${metrics['average_order_value']:,.2f}"
    )


with col7:

    st.metric(
        "📣 Marketing Spend",
        f"${metrics['marketing_spend']:,.0f}"
    )


with col8:

    st.metric(
        "🎯 ROAS",
        f"{metrics['roas']:.2f}x"
    )


# ============================================================
# DATASET PREVIEW
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔍 Data Preview'
    '</div>',
    unsafe_allow_html=True
)

with st.expander(
    "View filtered dataset"
):

    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True
    )

# ============================================================
# REVENUE & SALES ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📈 Revenue & Sales Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Explore revenue, order volume, and sales trends "
    "for the selected analysis period."
)

# ============================================================
# REVENUE TREND
# ============================================================

fig_revenue = revenue_trend_chart(
    filtered_df
)

st.plotly_chart(
    fig_revenue,
    width="stretch"
)

# ============================================================
# MOVING AVERAGE
# ============================================================

fig_moving_average = revenue_moving_average_chart(
    filtered_df,
    window=7
)

st.plotly_chart(
    fig_moving_average,
    width="stretch"
)

# ============================================================
# SALES ANALYSIS COLUMNS
# ============================================================

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    fig_orders = orders_trend_chart(
        filtered_df
    )

    st.plotly_chart(
        fig_orders,
        width="stretch"
    )


with chart_col2:

    fig_weekly = weekly_revenue_chart(
        filtered_df
    )

    st.plotly_chart(
        fig_weekly,
        width="stretch"
    )


# ============================================================
# REVENUE PERFORMANCE SUMMARY
# ============================================================

best_revenue_day = filtered_df.loc[
    filtered_df["revenue"].idxmax()
]

worst_revenue_day = filtered_df.loc[
    filtered_df["revenue"].idxmin()
]

st.markdown(
    "### 🔎 Revenue Highlights"
)

highlight_col1, highlight_col2 = st.columns(2)


with highlight_col1:

    st.info(
        f"**Best Revenue Day**\n\n"
        f"{best_revenue_day['date'].strftime('%d %b %Y')}\n\n"
        f"${best_revenue_day['revenue']:,.2f}"
    )


with highlight_col2:

    st.info(
        f"**Lowest Revenue Day**\n\n"
        f"{worst_revenue_day['date'].strftime('%d %b %Y')}\n\n"
        f"${worst_revenue_day['revenue']:,.2f}"
    )

    
# ============================================================
# REVENUE VS ORDERS
# ============================================================

fig_revenue_orders = revenue_orders_chart(
    filtered_df
)

st.plotly_chart(
    fig_revenue_orders,
    width="stretch"
)

# ============================================================
# REVENUE DISTRIBUTION
# ============================================================

fig_distribution = revenue_distribution_chart(
    filtered_df
)

st.plotly_chart(
    fig_distribution,
    width="stretch"
)

# ============================================================
# MARKETING SPEND TREND
# ============================================================

def marketing_spend_chart(df):
    """
    Display daily marketing spend over time.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["marketing_spend"],
            mode="lines+markers",
            name="Marketing Spend",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Marketing Spend: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Daily Marketing Spend",
        xaxis_title="Date",
        yaxis_title="Marketing Spend ($)",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# ROAS TREND
# ============================================================

def roas_trend_chart(df):
    """
    Display daily Return on Ad Spend.
    """

    data = df.copy()

    data["roas"] = (
        data["revenue"] /
        data["marketing_spend"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["roas"],
            mode="lines+markers",
            name="ROAS",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "ROAS: %{y:.2f}x"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=1,
        line_dash="dash",
        annotation_text="Break-even ROAS"
    )

    fig.update_layout(
        title="Daily ROAS Trend",
        xaxis_title="Date",
        yaxis_title="ROAS (x)",
        hovermode="x unified",
        template="plotly_white",
        height=420
    )

    return fig


# ============================================================
# REVENUE VS MARKETING SPEND
# ============================================================

def revenue_vs_marketing_chart(df):
    """
    Compare revenue and marketing spend.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["revenue"],
            mode="lines",
            name="Revenue",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Revenue: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["marketing_spend"],
            mode="lines",
            name="Marketing Spend",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Marketing Spend: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Revenue vs Marketing Spend",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        hovermode="x unified",
        template="plotly_white",
        height=450
    )

    return fig


# ============================================================
# MARKETING SPEND VS REVENUE SCATTER
# ============================================================

def marketing_efficiency_scatter(df):
    """
    Show the relationship between marketing spend
    and revenue.
    """

    fig = px.scatter(
        df,
        x="marketing_spend",
        y="revenue",
        title="Marketing Spend vs Revenue",
        labels={
            "marketing_spend": "Marketing Spend ($)",
            "revenue": "Revenue ($)"
        }
    )

    fig.update_traces(
        hovertemplate=(
            "Marketing Spend: $%{x:,.2f}<br>"
            "Revenue: $%{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ============================================================
# WEEKLY MARKETING SPEND
# ============================================================

def weekly_marketing_chart(df):
    """
    Aggregate marketing spend by week.
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
        ["marketing_spend"]
        .sum()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=weekly["week"],
            y=weekly["marketing_spend"],
            name="Marketing Spend",
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>"
                "Marketing Spend: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Weekly Marketing Spend",
        xaxis_title="Week",
        yaxis_title="Marketing Spend ($)",
        template="plotly_white",
        height=420
    )

    return fig

# ============================================================
# MARKETING PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📣 Marketing Performance'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Analyze marketing investment, revenue generation, "
    "and advertising efficiency."
)

fig_marketing_spend = marketing_spend_chart(
    filtered_df
)

st.plotly_chart(
    fig_marketing_spend,
    width="stretch"
)

marketing_col1, marketing_col2 = st.columns(2)


with marketing_col1:

    fig_roas = roas_trend_chart(
        filtered_df
    )

    st.plotly_chart(
        fig_roas,
        width="stretch"
    )


with marketing_col2:

    fig_weekly_marketing = weekly_marketing_chart(
        filtered_df
    )

    st.plotly_chart(
        fig_weekly_marketing,
        width="stretch"
    )

fig_revenue_marketing = revenue_vs_marketing_chart(
    filtered_df
)

st.plotly_chart(
    fig_revenue_marketing,
    width="stretch"
)

fig_marketing_scatter = marketing_efficiency_scatter(
    filtered_df
)

st.plotly_chart(
    fig_marketing_scatter,
    width="stretch"
)

# ============================================================
# MARKETING SUMMARY
# ============================================================

total_marketing_spend = (
    filtered_df["marketing_spend"].sum()
)

total_revenue = (
    filtered_df["revenue"].sum()
)

overall_roas = (
    total_revenue /
    total_marketing_spend
    if total_marketing_spend > 0
    else 0
)

roas_data = filtered_df.copy()

roas_data["daily_roas"] = (
    roas_data["revenue"] /
    roas_data["marketing_spend"].replace(
        0,
        float("nan")
    )
)

roas_data = roas_data.dropna(
    subset=["daily_roas"]
)

if not roas_data.empty:

    best_roas_day = roas_data.loc[
        roas_data["daily_roas"].idxmax()
    ]

else:

    best_roas_day = None


st.markdown(
    "### 🔎 Marketing Highlights"
)

summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.info(
        f"**Total Marketing Spend**\n\n"
        f"${total_marketing_spend:,.2f}"
    )


with summary_col2:

    st.info(
        f"**Overall ROAS**\n\n"
        f"{overall_roas:.2f}x"
    )


with summary_col3:

    if best_roas_day is not None:

        st.info(
            f"**Best ROAS Day**\n\n"
            f"{best_roas_day['date'].strftime('%d %b %Y')} "
            f"({best_roas_day['daily_roas']:.2f}x)"
        )

    else:

        st.info(
            "**Best ROAS Day**\n\n"
            "Not available"
        )

# ============================================================
# CUSTOMER & CONVERSION ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '👥 Customer & Conversion Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Understand customer growth, conversion performance, "
    "traffic quality, and order value."
)

# ============================================================
# CUSTOMER TREND
# ============================================================

fig_customer_trend = customer_trend_chart(
    filtered_df
)

st.plotly_chart(
    fig_customer_trend,
    width="stretch"
)

# ============================================================
# CUSTOMER MIX
# ============================================================

fig_customer_mix = customer_mix_chart(
    filtered_df
)

st.plotly_chart(
    fig_customer_mix,
    width="stretch"
)

# ============================================================
# CONVERSION + AOV
# ============================================================

customer_col1, customer_col2 = st.columns(2)


with customer_col1:

    fig_conversion = conversion_rate_chart(
        filtered_df
    )

    st.plotly_chart(
        fig_conversion,
        width="stretch"
    )


with customer_col2:

    fig_aov = aov_trend_chart(
        filtered_df
    )

    st.plotly_chart(
        fig_aov,
        width="stretch"
    )

# ============================================================
# TRAFFIC VS ORDERS
# ============================================================

fig_traffic_orders = traffic_vs_orders_chart(
    filtered_df
)

st.plotly_chart(
    fig_traffic_orders,
    width="stretch"
)

# ============================================================
# CUSTOMER SUMMARY
# ============================================================

total_new_customers = int(
    filtered_df["new_customers"].sum()
)

total_returning_customers = int(
    filtered_df["returning_customers"].sum()
)

total_customers = int(
    filtered_df["new_customers"].sum()
    + filtered_df["returning_customers"].sum()
)

total_traffic = int(
    filtered_df["website_traffic"].sum()
)

total_orders = int(
    filtered_df["orders"].sum()
)

overall_conversion = (
    total_orders /
    total_traffic *
    100
    if total_traffic > 0
    else 0
)

overall_aov = (
    filtered_df["revenue"].sum() /
    total_orders
    if total_orders > 0
    else 0
)

summary1, summary2, summary3, summary4 = st.columns(4)


with summary1:

    st.metric(
        "🆕 New Customers",
        f"{total_new_customers:,}"
    )


with summary2:

    st.metric(
        "🔄 Returning Customers",
        f"{total_returning_customers:,}"
    )


with summary3:

    st.metric(
        "🎯 Overall Conversion",
        f"{overall_conversion:.2f}%"
    )


with summary4:

    st.metric(
        "💵 Overall AOV",
        f"${overall_aov:,.2f}"
    )

new_customer_share = (
    total_new_customers /
    (
        total_new_customers +
        total_returning_customers
    ) *
    100
    if (
        total_new_customers +
        total_returning_customers
    ) > 0
    else 0
)

returning_customer_share = (
    100 -
    new_customer_share
)

mix1, mix2 = st.columns(2)


with mix1:

    st.info(
        f"**New Customer Share**\n\n"
        f"{new_customer_share:.1f}%"
    )


with mix2:

    st.info(
        f"**Returning Customer Share**\n\n"
        f"{returning_customer_share:.1f}%"
    )

# ============================================================
# CUSTOMER HIGHLIGHTS
# ============================================================

st.markdown(
    "### 🔎 Customer Highlights"
)

if overall_conversion >= 5:

    conversion_message = (
        "Conversion performance is relatively strong "
        "for the selected period."
    )

elif overall_conversion >= 2:

    conversion_message = (
        "Conversion performance is moderate. "
        "There may be opportunities to improve "
        "the customer journey."
    )

else:

    conversion_message = (
        "Conversion is relatively low. "
        "The business should investigate traffic quality "
        "and website conversion barriers."
    )


if returning_customer_share >= 40:

    retention_message = (
        "Returning customers represent a significant "
        "share of customer activity."
    )

else:

    retention_message = (
        "Customer activity is weighted toward new customers. "
        "Retention strategies may be worth exploring."
    )


st.info(
    f"**Conversion:** {conversion_message}"
)

st.info(
    f"**Customer Mix:** {retention_message}"
)

# ============================================================
# FORECAST MODEL EVALUATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🧪 Forecast Model Evaluation'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Models are evaluated using a chronological "
    "historical validation period."
)

try:

    model_results = compare_forecasting_models(
        filtered_df,
        validation_ratio=0.2,
        window=7
    )

    comparison_df = model_results[
        "comparison"
    ]

    best_model = model_results[
        "best_model"
    ]

except ValueError as error:

    st.error(
        f"Model evaluation failed: {error}"
    )

    st.stop()

st.dataframe(
    comparison_df.style.format(
        {
            "mae": "${:,.2f}",
            "rmse": "${:,.2f}",
            "r2": "{:.3f}"
        }
    ),
    width="stretch",
    hide_index=True
)

st.success(
    f"🏆 Best Forecasting Model: **{best_model}**"
)

if best_model == "7-Day Moving Average":

    validation_data = model_results[
        "moving_average_validation"
    ]

else:

    validation_data = model_results[
        "linear_validation"
    ]

fig_validation = model_validation_chart(
    validation_data,
    best_model
)

st.plotly_chart(
    fig_validation,
    width="stretch"
)

# ============================================================
# REVENUE FORECAST
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔮 Revenue Forecast'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Estimate revenue for the next 30 days "
    "using a 7-day moving-average baseline."
)

st.success(
    f"🏆 Selected Forecast Model: **{best_model}**"
)

# ============================================================
# GENERATE FORECAST
# ============================================================
try:

    forecast_results = generate_best_forecast(
        df,
        periods=30,
        validation_ratio=0.2,
        window=7
    )

    best_model = forecast_results[
        "best_model"
    ]

    forecast_df = forecast_results[
        "forecast"
    ]

    combined_forecast = forecast_results[
        "combined"
    ]

    summary = forecast_results[
        "summary"
    ]

except ValueError as error:

    st.error(
        f"Unable to generate forecast: {error}"
    )

    st.stop()

fig_forecast = forecast_chart(
    combined_forecast
)

st.plotly_chart(
    fig_forecast,
    width="stretch"
)

forecast_col1, forecast_col2, forecast_col3, forecast_col4 = st.columns(4)


with forecast_col1:

    st.metric(
        "🤖 Selected Model",
        best_model
    )


with forecast_col2:

    st.metric(
        "📅 Forecast Period",
        "30 Days"
    )


with forecast_col3:

    st.metric(
        "💰 Expected Revenue",
        f"${summary['total_forecast']:,.2f}"
    )


with forecast_col4:

    st.metric(
        "📊 Avg Daily Revenue",
        f"${summary['average_daily_forecast']:,.2f}"
    )

forecast_min = summary[
    "minimum_daily_forecast"
]

forecast_max = summary[
    "maximum_daily_forecast"
]

st.info(
    f"Expected daily revenue range: "
    f"**${forecast_min:,.2f} - "
    f"${forecast_max:,.2f}**"
)

historical_total = (
    filtered_df["revenue"]
    .sum()
)

forecast_total = (
    forecast_df["forecast"]
    .sum()
)

historical_days = len(
    filtered_df
)

historical_daily_average = (
    historical_total /
    historical_days
    if historical_days > 0
    else 0
)

forecast_daily_average = (
    forecast_total /
    len(forecast_df)
    if len(forecast_df) > 0
    else 0
)

forecast_change = (
    (
        forecast_daily_average -
        historical_daily_average
    )
    /
    historical_daily_average
    *
    100
    if historical_daily_average > 0
    else 0
)

st.markdown(
    "### 📈 Historical vs Forecast"
)

comparison_col1, comparison_col2 = st.columns(2)


with comparison_col1:

    st.metric(
        "Historical Daily Average",
        f"${historical_daily_average:,.2f}"
    )


with comparison_col2:

    st.metric(
        "Forecast Daily Average",
        f"${forecast_daily_average:,.2f}",
        delta=f"{forecast_change:+.2f}%"
    )


st.markdown(
    "### 🔎 Forecast Interpretation"
)

historical_average = (
    filtered_df["revenue"].mean()
)

forecast_average = (
    forecast_df["forecast"].mean()
)

forecast_change = (
    (
        forecast_average -
        historical_average
    )
    /
    historical_average
    *
    100
    if historical_average > 0
    else 0
)

# ============================================================
# FORECAST MODEL METADATA
# ============================================================

model_metadata = {
    "selected_model": best_model,
    "forecast_days": len(forecast_df),
    "forecast_total": summary[
        "total_forecast"
    ],
    "forecast_daily_average": summary[
        "average_daily_forecast"
    ],
    "historical_daily_average":
        historical_daily_average,
    "forecast_change_percent":
        forecast_change
}

if forecast_change > 5:

    forecast_status = (
        "📈 Forecast indicates stronger average "
        "daily revenue than the historical period."
    )

elif forecast_change < -5:

    forecast_status = (
        "📉 Forecast indicates weaker average "
        "daily revenue than the historical period."
    )

else:

    forecast_status = (
        "➡️ Forecast remains broadly consistent "
        "with the historical revenue level."
    )

st.info(
    forecast_status
)

st.caption(
    "Forecasts are statistical estimates based on "
    "historical revenue patterns and should not be "
    "treated as guaranteed future revenue."
)

from validation import validate_forecast
forecast_validation = validate_forecast(
    forecast_df,
    forecast_column="forecast",
    expected_days=30
)

if not forecast_validation["passed"]:

    st.error(
        "⚠️ Forecast validation failed."
    )

    for check in forecast_validation["checks"]:

        if not check["passed"]:

            st.warning(
                f"{check['check']}: "
                f"{check['message']}"
            )

    st.stop()

# ============================================================
# VERIFIED BUSINESS METRICS FOR AI
# ============================================================

ai_metrics = {
    "total_revenue": float(
        filtered_df["revenue"].sum()
    ),

    "total_orders": int(
        filtered_df["orders"].sum()
    ),

    "total_traffic": int(
        filtered_df["website_traffic"].sum()
    ),

    "total_marketing_spend": float(
        filtered_df["marketing_spend"].sum()
    ),

    "overall_conversion_rate": float(
        overall_conversion
    ),

    "overall_aov": float(
        overall_aov
    ),

    "new_customers": int(
        filtered_df["new_customers"].sum()
    ),

    "returning_customers": int(
        filtered_df["returning_customers"].sum()
    ),

    "returning_customer_share": float(
        returning_customer_share
    )
}

# ============================================================
# AI BUSINESS INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🤖 AI Business Insights'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "AI-generated interpretation based on verified "
    "dashboard metrics and the selected forecast model."
)

generate_insights = st.button(
    "✨ Generate / Refresh AI Insights",
    type="primary"
)

if generate_insights:

    with st.spinner(
        "Analyzing business performance..."
    ):

        try:

            ai_report = generate_business_insights(
                metrics=ai_metrics,
                model_metadata=model_metadata
            )

            st.session_state[
                "ai_business_report"
            ] = ai_report

            st.session_state[
                "ai_report_generated_at"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except Exception as error:

            st.error(
                "AI insights could not be generated. "
                "The dashboard metrics and forecasting features "
                "are still available."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(
                    str(error)
                )

if (
    "ai_business_report"
    in st.session_state
):

    generated_at = st.session_state.get(
        "ai_report_generated_at",
        ""
    )

    if generated_at:

        st.caption(
            f"Generated: {generated_at}"
        )

    st.markdown(
        prepare_ai_report_for_display(
            st.session_state[
                "ai_business_report"
            ]
        )
    )

# ============================================================
# PDF REPORT EXPORT
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📄 Export Business Report'
    '</div>',
    unsafe_allow_html=True
)

ai_report_for_pdf = st.session_state.get(
    "ai_business_report",
    None
)

if ai_report_for_pdf:

    try:

        pdf_path = create_report_file(
            metrics=ai_metrics,
            model_metadata=model_metadata,
            ai_report=ai_report_for_pdf,
            revenue_chart=fig_revenue,
            marketing_chart=fig_marketing_spend,
            customer_chart=fig_customer_trend,
            forecast_chart=fig_forecast
        )

        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            pdf_bytes = pdf_file.read()

        st.download_button(
            label="📥 Download PDF Business Report",
            data=pdf_bytes,
            file_name=(
                "AI_Business_Intelligence_Report.pdf"
            ),
            mime="application/pdf"
        )

        os.unlink(
            pdf_path
        )

    except Exception as error:

        st.error(
            "The PDF report could not be generated."
        )

        with st.expander(
            "Technical details"
        ):

            st.code(
                str(error)
            )

else:

    st.info(
        "Generate AI Business Insights first, "
        "then you can export the complete PDF report."
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Business Intelligence Dashboard | "
    "E-Commerce Analytics Prototype"
)