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


def generate_features_pdf():
    buffer = open("school_management_features.pdf", "wb")
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
    subheading_style = ParagraphStyle(
        "Subheading",
        parent=styles["Heading3"],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.HexColor("#1565c0"),
    )
    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=6,
    )

    elements = []
    elements.append(Paragraph("School Management System", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Suggested Features for Enhancement", title_style))
    elements.append(Spacer(1, 30))

    # High Value Section
    elements.append(Paragraph("HIGH VALUE FEATURES", heading_style))
    elements.append(Spacer(1, 10))

    high_value_data = [
        ["#", "Feature", "Description"],
        ["1", "SMS/Email Notifications", "Send attendance alerts, fee reminders to parents via Twilio/SendGrid"],
        ["2", "Online Payments", "Integrate Stripe/PayPal for fee collection"],
        ["3", "Parent Portal", "Real-time attendance, fees, grades viewing for parents"],
        ["4", "Student ID Cards", "Generate printable PDF ID cards"],
        ["5", "Online Quiz System", "Self-paced quizzes with instant results"],
    ]

    table = Table(high_value_data, colWidths=[0.5*inch, 2*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1976d2")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e3f2fd")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 25))

    # Useful Section
    elements.append(Paragraph("USEFUL FEATURES", heading_style))
    elements.append(Spacer(1, 10))

    useful_data = [
        ["#", "Feature", "Description"],
        ["1", "Hostel Management", "Room allocation, bed management, attendance"],
        ["2", "Transport Tracking", "GPS tracking, route maps with parent app"],
        ["3", "Exam Seating Plan", "Auto-generate exam seating arrangements"],
        ["4", "Certificate Generation", "Generate transfer certificates, character certificates"],
        ["5", "Inventory/Asset Management", "Track school equipment, books, furniture"],
    ]

    table = Table(useful_data, colWidths=[0.5*inch, 2*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#388e3c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e8f5e9")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 25))

    # Advanced Section
    elements.append(Paragraph("ADVANCED FEATURES", heading_style))
    elements.append(Spacer(1, 10))

    advanced_data = [
        ["#", "Feature", "Description"],
        ["1", "Mobile App", "React Native/Flutter apps for parents/students"],
        ["2", "AI Analytics", "Predict student performance, at-risk alerts"],
        ["3", "Library QR Scanning", "Quick book issue/return"],
        ["4", "Online Admission", "Public portal for new student applications"],
    ]

    table = Table(advanced_data, colWidths=[0.5*inch, 2*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7b1fa2")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3e5f5")]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 30))

    # Footer
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )
    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        footer_style,
    ))
    elements.append(Paragraph(
        "School Management System",
        footer_style,
    ))

    doc.build(elements)
    buffer.close()
    print("PDF created: school_management_features.pdf")


if __name__ == "__main__":
    generate_features_pdf()