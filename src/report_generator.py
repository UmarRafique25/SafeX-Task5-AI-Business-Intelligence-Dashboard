"""
report_generator.py

Generate a professional PDF business intelligence report.
"""

import os
import tempfile
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    Image
)


# ============================================================
# REPORT STYLES
# ============================================================

def get_report_styles():
    """
    Create styles used throughout the PDF.
    """

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=12
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=20
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontSize=15,
            leading=18,
            spaceBefore=12,
            spaceAfter=8
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyTextCustom",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            spaceAfter=7
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["Normal"],
            fontSize=8,
            leading=11
        )
    )

    return styles


# ============================================================
# SAFE TEXT
# ============================================================

def clean_text(value):
    """
    Convert values to PDF-safe text.
    """

    if value is None:
        return ""

    return str(value).replace(
        "&",
        "&amp;"
    ).replace(
        "<",
        "&lt;"
    ).replace(
        ">",
        "&gt;"
    )

# ============================================================
# PLOTLY CHART TO IMAGE
# ============================================================

def save_plotly_chart(
    figure,
    filename,
    width=1200,
    height=600
):
    """
    Convert a Plotly figure into a PNG image.

    Parameters
    ----------
    figure:
        Plotly Figure object.

    filename:
        Destination PNG path.

    width:
        Image width.

    height:
        Image height.

    Returns
    -------
    str
        Saved image path.
    """

    if figure is None:
        return None

    figure.write_image(
        filename,
        width=width,
        height=height,
        scale=2
    )

    return filename

# ============================================================
# ADD CHART TO PDF
# ============================================================

def add_chart_to_pdf(
    story,
    figure,
    title,
    styles,
    width=7.0 * inch,
    height=3.5 * inch
):
    """
    Convert a Plotly figure to PNG and add it
    to the PDF story.
    """

    if figure is None:
        return

    temporary_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    )

    temporary_file.close()

    image_path = save_plotly_chart(
        figure,
        temporary_file.name
    )

    story.append(
        KeepTogether(
            [
                Paragraph(
                    clean_text(title),
                    styles["SectionHeading"]
                ),
                Image(
                    image_path,
                    width=width,
                    height=height
                ),
                Spacer(
                    1,
                    10
                )
            ]
        )
    )

# ============================================================
# KPI TABLE
# ============================================================

def build_kpi_table(
    metrics,
    styles
):
    """
    Build KPI summary table.
    """

    rows = [
        [
            "Metric",
            "Value"
        ]
    ]

    metric_labels = {
        "total_revenue":
            "Total Revenue",

        "total_orders":
            "Total Orders",

        "total_traffic":
            "Total Traffic",

        "total_marketing_spend":
            "Marketing Spend",

        "overall_conversion_rate":
            "Conversion Rate",

        "overall_aov":
            "Average Order Value",

        "new_customers":
            "New Customers",

        "returning_customers":
            "Returning Customers",

        "returning_customer_share":
            "Returning Customer Share"
    }

    for key, label in metric_labels.items():

        if key not in metrics:
            continue

        value = metrics[key]

        if "rate" in key or "share" in key:

            formatted_value = (
                f"{value:.2f}%"
            )

        elif (
            "revenue" in key
            or "spend" in key
            or "aov" in key
        ):

            formatted_value = (
                f"${value:,.2f}"
            )

        else:

            formatted_value = (
                f"{value:,}"
            )

        rows.append(
            [
                Paragraph(
                    clean_text(label),
                    styles["SmallText"]
                ),
                Paragraph(
                    clean_text(formatted_value),
                    styles["SmallText"]
                )
            ]
        )

    table = Table(
        rows,
        colWidths=[
            3.8 * inch,
            2.2 * inch
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F2937")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )

    return table


# ============================================================
# FORECAST TABLE
# ============================================================

def build_forecast_table(
    model_metadata,
    styles
):
    """
    Build forecast summary table.
    """

    rows = [
        [
            "Forecast Metric",
            "Value"
        ],
        [
            "Selected Model",
            model_metadata[
                "selected_model"
            ]
        ],
        [
            "Forecast Period",
            f"{model_metadata['forecast_days']} Days"
        ],
        [
            "Forecast Revenue",
            (
                f"${model_metadata['forecast_total']:,.2f}"
            )
        ],
        [
            "Average Daily Forecast",
            (
                f"${model_metadata['forecast_daily_average']:,.2f}"
            )
        ],
        [
            "Historical Daily Average",
            (
                f"${model_metadata['historical_daily_average']:,.2f}"
            )
        ],
        [
            "Forecast Change",
            (
                f"{model_metadata['forecast_change_percent']:+.2f}%"
            )
        ]
    ]

    formatted_rows = []

    for row_index, row in enumerate(rows):

        formatted_rows.append(
            [
                Paragraph(
                    clean_text(cell),
                    styles["SmallText"]
                )
                for cell in row
            ]
        )

    table = Table(
        formatted_rows,
        colWidths=[
            3.8 * inch,
            2.2 * inch
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F2937")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )

    return table


# ============================================================
# AI REPORT SECTION
# ============================================================

def add_ai_report_section(
    story,
    ai_report,
    styles
):
    """
    Convert the AI-generated markdown-style report
    into readable PDF paragraphs.
    """

    if not ai_report:
        return

    lines = ai_report.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            story.append(
                Spacer(1, 6)
            )
            continue

        if line.startswith("## "):

            heading = line[
                3:
            ].strip()

            story.append(
                Paragraph(
                    clean_text(heading),
                    styles["SectionHeading"]
                )
            )

        elif line.startswith("- "):

            bullet = line[
                2:
            ].strip()

            story.append(
                Paragraph(
                    f"• {clean_text(bullet)}",
                    styles["BodyTextCustom"]
                )
            )

        else:

            story.append(
                Paragraph(
                    clean_text(line),
                    styles["BodyTextCustom"]
                )
            )


# ============================================================
# FOOTER
# ============================================================

def add_page_number(
    canvas,
    doc
):
    """
    Add page number to every page.
    """

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.drawString(
        0.7 * inch,
        0.45 * inch,
        "AI Business Intelligence Dashboard"
    )

    canvas.drawRightString(
        7.8 * inch,
        0.45 * inch,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ============================================================
# GENERATE PDF
# ============================================================

def generate_pdf_report(
    output_path,
    metrics,
    model_metadata,
    ai_report=None,
    revenue_chart=None,
    marketing_chart=None,
    customer_chart=None,
    forecast_chart=None,
    report_title=(
        "AI Business Intelligence Report"
    ),
    report_period="Selected Analysis Period"
):
    """
    Generate a complete PDF business report.
    """

    output_directory = os.path.dirname(
        output_path
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    styles = get_report_styles()

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.7 * inch
    )

    story = []

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    story.append(
        Spacer(
            1,
            0.5 * inch
        )
    )

    story.append(
        Paragraph(
            clean_text(report_title),
            styles["ReportTitle"]
        )
    )

    story.append(
        Paragraph(
            clean_text(
                f"Report Period: {report_period}"
            ),
            styles["ReportSubtitle"]
        )
    )

    story.append(
        Paragraph(
            clean_text(
                "Generated: "
                + datetime.now().strftime(
                    "%d %B %Y, %H:%M"
                )
            ),
            styles["ReportSubtitle"]
        )
    )

    # --------------------------------------------------------
    # KPI SECTION
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Key Performance Indicators",
            styles["SectionHeading"]
        )
    )

    story.append(
        build_kpi_table(
            metrics,
            styles
        )
    )

    story.append(
        Spacer(
            1,
            12
        )
    )

    add_chart_to_pdf(
        story,
        revenue_chart,
        "Revenue Performance",
        styles,
        width=6.7 * inch,
        height=3.0 * inch
    )

    # --------------------------------------------------------
    # FORECAST SECTION
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "30-Day Forecast",
            styles["SectionHeading"]
        )
    )

    story.append(
        build_forecast_table(
            model_metadata,
            styles
        )
    )

    story.append(
        Spacer(
            1,
            12
        )
    )

    story.append(
        Paragraph(
            clean_text(
                "Forecasts are statistical estimates "
                "based on historical business data and "
                "should not be treated as guaranteed "
                "future results."
            ),
            styles["BodyTextCustom"]
        )
    )

    # --------------------------------------------------------
    # AI INSIGHTS
    # --------------------------------------------------------
    add_chart_to_pdf(
        story,
        marketing_chart,
        "Marketing Performance",
        styles
    )

    add_chart_to_pdf(
        story,
        customer_chart,
        "Customer Performance",
        styles
    )

    story.append(
        Paragraph(
            "Forecast Analysis",
            styles["SectionHeading"]
        )
    )

    add_chart_to_pdf(
        story,
        forecast_chart,
        "30-Day Revenue Forecast",
        styles
    )

    story.append(
        Paragraph(
            "AI Business Insights",
            styles["SectionHeading"]
        )
    )

    if ai_report:

        add_ai_report_section(
            story,
            ai_report,
            styles
        )

    else:

        story.append(
            Paragraph(
                "AI insights were not generated "
                "for this report.",
                styles["BodyTextCustom"]
            )
        )

    # --------------------------------------------------------
    # BUILD
    # --------------------------------------------------------

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return output_path