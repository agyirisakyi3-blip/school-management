from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


def generate_ui_ux_suggestions_pdf():
    buffer = open("ui_ux_suggestions.pdf", "wb")
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#1a237e"),
    )
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.HexColor("#0d47a1"),
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Heading3"],
        fontSize=12,
        spaceAfter=6,
        textColor=colors.HexColor("#1565c0"),
    )
    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=4,
        leftIndent=20,
    )

    elements = []
    elements.append(Paragraph("School Management System", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("UI/UX Suggestions", title_style))
    elements.append(Spacer(1, 30))

    # Dashboard Improvements
    elements.append(Paragraph("DASHBOARD IMPROVEMENTS", heading_style))
    elements.append(Spacer(1, 8))

    dashboard_data = [
        ["#", "Suggestion", "Implementation"],
        ["1", "Welcome banner with today's summary", "Show date, weather icon, quick stats cards"],
        ["2", "Quick action buttons", "Add Student, Record Attendance, Create Fee, Send Notice"],
        ["3", "Interactive charts", "Attendance pie chart, Fee collection bar graph"],
        ["4", "Recent activity feed", "Live updates sidebar with icons"],
        ["5", "Quick links grid", "Popular actions as icon cards"],
    ]

    table = Table(dashboard_data, colWidths=[0.4*inch, 2.2*inch, 3.4*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e3f2fd")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Color Scheme
    elements.append(Paragraph("COLOR SCHEME RECOMMENDATIONS", heading_style))
    elements.append(Spacer(1, 8))

    color_data = [
        ["Element", "Color", "Hex Code", "Usage"],
        ["Primary Blue", "Deep Blue", "#1565c0", "Headers, buttons, links"],
        ["Secondary", "Teal", "#00897b", "Success states, accents"],
        ["Background", "Light Gray", "#f5f5f5", "Page backgrounds"],
        ["Card White", "White", "#ffffff", "Cards, tables"],
        ["Warning", "Amber", "#ff8f00", "Pending, overdue"],
        ["Danger", "Red", "#d32f2f", "Errors, delete"],
    ]

    table = Table(color_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1.8*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e7d32")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e8f5e9")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Responsive Design
    elements.append(Paragraph("RESPONSIVE DESIGN", heading_style))
    elements.append(Spacer(1, 8))

    responsive_data = [
        ["Screen Size", "Columns", "Layout"],
        ["Desktop (>1024px)", "4 columns", "Full sidebar + content"],
        ["Tablet (768-1024px)", "2 columns", "Collapsible sidebar"],
        ["Mobile (<768px)", "1 column", "Hidden sidebar, hamburger menu"],
    ]

    table = Table(responsive_data, colWidths=[1.4*inch, 1.3*inch, 2.8*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6a1b9a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3e5f5")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Navigation
    elements.append(Paragraph("NAVIGATION IMPROVEMENTS", heading_style))
    elements.append(Spacer(1, 8))

    nav_data = [
        ["#", "Feature", "Description"],
        ["1", "Breadcrumb trails", "Show current location path"],
        ["2", "Search everywhere", "Global search (Cmd+K) in header"],
        ["3", "User dropdown", "Profile, settings, logout menu"],
        ["4", "Dark mode toggle", "Light/dark theme switcher"],
        ["5", "Notifications bell", "Badge with unread count"],
    ]

    table = Table(nav_data, colWidths=[0.4*inch, 1.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#c62828")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#ffebee")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Tables
    elements.append(Paragraph("TABLE IMPROVEMENTS", heading_style))
    elements.append(Spacer(1, 8))

    table_data = [
        ["#", "Feature", "Description"],
        ["1", "Sortable columns", "Click header to sort ASC/DESC"],
        ["2", "Row hover highlight", "Highlight row on mouse over"],
        ["3", "Bulk actions", "Checkboxes + action dropdown"],
        ["4", "Inline edit", "Click cell to edit directly"],
        ["5", "Pagination", "10/25/50 per page options"],
    ]

    table = Table(table_data, colWidths=[0.4*inch, 1.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ef6c00")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fff3e0")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Footer
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        footer_style,
    ))

    doc.build(elements)
    buffer.close()
    print("PDF created: ui_ux_suggestions.pdf")


if __name__ == "__main__":
    generate_ui_ux_suggestions_pdf()