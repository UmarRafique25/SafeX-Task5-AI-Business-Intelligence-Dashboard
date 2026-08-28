from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import re


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent

MARKDOWN_FILE = BASE_DIR / "weekly_progress_report.md"
OUTPUT_FILE = BASE_DIR / "AI_Business_Intelligence_Weekly_Report.pdf"

EVIDENCE_DIR = PROJECT_DIR / "evidence"


# ============================================================
# OPTIONAL FONT
# ============================================================

FONT_NAME = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


# ============================================================
# DOCUMENT
# ============================================================

doc = SimpleDocTemplate(
    str(OUTPUT_FILE),
    pagesize=A4,
    rightMargin=45,
    leftMargin=45,
    topMargin=50,
    bottomMargin=50,
    title="AI Business Intelligence Dashboard - Weekly Progress Report",
    author="AI Business Intelligence Dashboard Project",
)


# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontName=FONT_BOLD,
    fontSize=24,
    leading=30,
    alignment=TA_CENTER,
    spaceAfter=20,
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName=FONT_NAME,
    fontSize=13,
    leading=18,
    alignment=TA_CENTER,
    spaceAfter=10,
)

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading1"],
    fontName=FONT_BOLD,
    fontSize=16,
    leading=20,
    spaceBefore=14,
    spaceAfter=10,
)

subheading_style = ParagraphStyle(
    "SubHeading",
    parent=styles["Heading2"],
    fontName=FONT_BOLD,
    fontSize=12,
    leading=16,
    spaceBefore=10,
    spaceAfter=6,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName=FONT_NAME,
    fontSize=9.5,
    leading=14,
    spaceAfter=8,
)

bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=15,
    firstLineIndent=-8,
    spaceAfter=4,
)

small_style = ParagraphStyle(
    "Small",
    parent=body_style,
    fontSize=8,
    leading=11,
)


# ============================================================
# HELPERS
# ============================================================

def escape_text(text):
    """
    Escape characters that can interfere with ReportLab
    paragraph markup.
    """
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def markdown_inline(text):
    """
    Basic Markdown formatting conversion.
    """
    text = escape_text(text)

    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text,
    )

    text = re.sub(
        r"\*(.*?)\*",
        r"<i>\1</i>",
        text,
    )

    text = re.sub(
        r"`(.*?)`",
        r"<font name='Courier'>\1</font>",
        text,
    )

    return text


def add_page_number(canvas, document):
    """
    Add page numbers to every page.
    """
    page_number = canvas.getPageNumber()

    canvas.saveState()

    canvas.setFont(FONT_NAME, 8)

    canvas.drawCentredString(
        A4[0] / 2,
        25,
        f"AI Business Intelligence Dashboard | Page {page_number}",
    )

    canvas.restoreState()


def find_evidence_image(filename):
    """
    Resolve an evidence screenshot from the report reference.
    """
    requested_path = Path(filename)
    candidates = [
        (MARKDOWN_FILE.parent / requested_path).resolve(),
        PROJECT_DIR / "screenshots" / requested_path.name,
        EVIDENCE_DIR / f"{requested_path.stem}_page1{requested_path.suffix}",
        PROJECT_DIR / "screenshots" / f"{requested_path.stem}_page1{requested_path.suffix}",
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


# ============================================================
# BUILD STORY
# ============================================================

story = []


# ============================================================
# COVER PAGE
# ============================================================

story.append(Spacer(1, 1.2 * inch))

story.append(
    Paragraph(
        "AI BUSINESS<br/>INTELLIGENCE DASHBOARD",
        title_style,
    )
)

story.append(
    Paragraph(
        "Weekly Progress Report",
        subtitle_style,
    )
)

story.append(Spacer(1, 0.3 * inch))

story.append(
    Paragraph(
        "<b>Week 5</b>",
        subtitle_style,
    )
)

story.append(
    Paragraph(
        "AI / Business Intelligence / Data Analytics",
        subtitle_style,
    )
)

story.append(Spacer(1, 0.5 * inch))

cover_data = [
    ["Project Type", "Advanced AI/BI Prototype"],
    ["Development Duration", "6–7 Days"],
    ["Primary Platform", "Streamlit"],
    ["Deployment", "Streamlit Community Cloud"],
    ["Repository", "GitHub"],
]

table = Table(
    cover_data,
    colWidths=[2.0 * inch, 3.5 * inch],
)

table.setStyle(
    TableStyle(
        [
            ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
            ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)

story.append(table)

story.append(Spacer(1, 0.6 * inch))

story.append(
    Paragraph(
        "Prepared for SafeX / University Evaluation",
        subtitle_style,
    )
)

story.append(PageBreak())


# ============================================================
# TABLE OF CONTENTS
# ============================================================

story.append(
    Paragraph(
        "Table of Contents",
        heading_style,
    )
)

toc_items = [
    "1. Project Overview",
    "2. Problem Statement",
    "3. Target Customers",
    "4. Business Value",
    "5. Project Objectives",
    "6. Technologies and Tools",
    "7. Development Process",
    "8. Major Features Implemented",
    "9. System Workflow",
    "10. Forecasting",
    "11. AI-Generated Business Insights",
    "12. Testing and Validation",
    "13. Problems Encountered and Solutions",
    "14. Deployment",
    "15. Commercial Potential",
    "16. Project Results",
    "17. Project Screenshots",
    "18. Project Links",
    "19. Lessons Learned",
    "20. Next Week's Plan",
    "21. Conclusion",
]

for item in toc_items:
    story.append(
        Paragraph(
            item,
            body_style,
        )
    )

story.append(PageBreak())


# ============================================================
# READ MARKDOWN
# ============================================================

if not MARKDOWN_FILE.exists():
    raise FileNotFoundError(
        f"Markdown report not found: {MARKDOWN_FILE}"
    )

content = MARKDOWN_FILE.read_text(
    encoding="utf-8"
)

lines = content.splitlines()


# ============================================================
# PARSE MARKDOWN
# ============================================================

i = 0
last_heading_text = None

while i < len(lines):

    line = lines[i].strip()

    # Empty line
    if not line:
        story.append(Spacer(1, 4))
        i += 1
        continue

    # H1
    if line.startswith("# ") and not line.startswith("## "):
        text = line[2:].strip()

        # Skip duplicate main report title
        if "WEEKLY PROGRESS REPORT" not in text.upper():
            story.append(
                Paragraph(
                    markdown_inline(text),
                    heading_style,
                )
            )
            last_heading_text = text

        i += 1
        continue

    # H2
    if line.startswith("## "):
        text = line[3:].strip()

        story.append(
            Paragraph(
                markdown_inline(text),
                heading_style,
            )
        )
        last_heading_text = text

        i += 1
        continue

    # H3
    if line.startswith("### "):
        text = line[4:].strip()

        story.append(
            Paragraph(
                markdown_inline(text),
                subheading_style,
            )
        )
        last_heading_text = text

        i += 1
        continue

    # Bullet
    if line.startswith("- "):
        text = line[2:].strip()

        story.append(
            Paragraph(
                "• " + markdown_inline(text),
                bullet_style,
            )
        )

        i += 1
        continue

    # Numbered list
    if re.match(r"^\d+\.\s+", line):
        match = re.match(r"^(\d+)\.\s+(.*)", line)

        if match:
            number = match.group(1)
            text = match.group(2)

            story.append(
                Paragraph(
                    f"{number}. {markdown_inline(text)}",
                    bullet_style,
                )
            )

            i += 1
            continue

    # Table
    if "|" in line:

        table_rows = []

        while i < len(lines) and "|" in lines[i]:

            current = lines[i].strip()

            # Ignore markdown separator
            if not re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?$", current):
                cells = [
                    cell.strip()
                    for cell in current.strip("|").split("|")
                ]

                table_rows.append(
                    [
                        Paragraph(
                            markdown_inline(cell),
                            small_style,
                        )
                        for cell in cells
                    ]
                )

            i += 1

        if table_rows:

            column_count = max(
                len(row)
                for row in table_rows
            )

            width = 6.8 * inch / column_count

            table = Table(
                table_rows,
                colWidths=[width] * column_count,
                repeatRows=1,
            )

            table.setStyle(
                TableStyle(
                    [
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.4,
                            colors.grey,
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            FONT_BOLD,
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP",
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                    ]
                )
            )

            story.append(table)
            story.append(Spacer(1, 8))

        continue

    # Markdown image
    image_match = re.match(
        r"!\[(.*?)\]\((.*?)\)",
        line,
    )

    if image_match:
        caption = image_match.group(1)
        image_reference = image_match.group(2)

        image_path = find_evidence_image(image_reference)

        if caption.strip().casefold() != (last_heading_text or "").strip().casefold():
            story.append(
                Paragraph(
                    markdown_inline(caption),
                    subheading_style,
                )
            )

        if image_path:

            try:
                image = Image(
                    str(image_path),
                    width=6.3 * inch,
                    height=4.0 * inch,
                    kind="proportional",
                )

                story.append(image)
                story.append(Spacer(1, 12))

            except Exception as e:

                story.append(
                    Paragraph(
                        f"Unable to render image: {escape_text(str(e))}",
                        small_style,
                    )
                )

        else:

            story.append(
                Paragraph(
                    f"Image not found: {escape_text(image_reference)}",
                    small_style,
                )
            )

        i += 1
        continue


    # Markdown link
    link_match = re.match(
        r"\[(.*?)\]\((.*?)\)",
        line,
    )

    # Markdown link
    link_match = re.match(
        r"\[(.*?)\]\((.*?)\)",
        line,
    )

    if link_match:

        label = link_match.group(1)
        url = link_match.group(2)

        story.append(
            Paragraph(
                f"<b>{escape_text(label)}</b><br/>{escape_text(url)}",
                body_style,
            )
        )

        i += 1
        continue

    # Normal paragraph
    paragraph_lines = [line]

    i += 1

    while (
        i < len(lines)
        and lines[i].strip()
        and not lines[i].strip().startswith("#")
        and not lines[i].strip().startswith("- ")
        and not re.match(r"^\d+\.\s+", lines[i].strip())
        and "|" not in lines[i]
    ):
        paragraph_lines.append(lines[i].strip())
        i += 1

    paragraph_text = " ".join(paragraph_lines)

    story.append(
        Paragraph(
            markdown_inline(paragraph_text),
            body_style,
        )
    )


# ============================================================
# BUILD PDF
# ============================================================

doc.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number,
)

print()
print("=" * 60)
print("WEEKLY PROGRESS REPORT GENERATED")
print("=" * 60)
print(f"Output: {OUTPUT_FILE}")
print("=" * 60)