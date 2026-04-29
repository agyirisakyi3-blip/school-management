from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


def generate_user_manual():
    buffer = open("SchoolMS_User_Manual.pdf", "wb")
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=22, alignment=TA_CENTER, spaceAfter=20, textColor=colors.HexColor("#1565c0"))
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=16, spaceAfter=12, textColor=colors.HexColor("#0d47a1"))
    subheading_style = ParagraphStyle("Subheading", parent=styles["Heading3"], fontSize=13, spaceAfter=8, textColor=colors.HexColor("#1565c0"))
    normal_style = ParagraphStyle("Normal", parent=styles["Normal"], fontSize=10, spaceAfter=8)
    bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], fontSize=10, spaceAfter=4, leftIndent=20)

    elements = []
    
    # Title Page
    elements.append(Paragraph("🎓", ParagraphStyle("Icon", fontSize=60, alignment=TA_CENTER)))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("School Management System", title_style))
    elements.append(Paragraph("User Manual", title_style))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Version 1.0", normal_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("📧 Support: support@schoolms.com", normal_style))
    elements.append(Paragraph("🌐 Website: www.schoolms.com", normal_style))
    elements.append(PageBreak())

    # Table of Contents
    elements.append(Paragraph("Table of Contents", heading_style))
    elements.append(Spacer(1, 10))
    toc = [
        ["1.", "Introduction", "3"],
        ["2.", "Getting Started", "3"],
        ["3.", "User Roles", "4"],
        ["4.", "Admin Dashboard", "5"],
        ["5.", "Student Management", "7"],
        ["6.", "Teacher Management", "9"],
        ["7.", "Attendance", "10"],
        ["8.", "Exams & Results", "11"],
        ["9.", "Fee Management", "12"],
        ["10.", "Library", "13"],
        ["11.", "Communication", "14"],
    ]
    t = Table(toc, colWidths=[0.5*inch, 4*inch, 1*inch])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Section 1: Introduction
    elements.append(Paragraph("1. Introduction", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Welcome to the School Management System (SchoolMS). This comprehensive software helps schools manage student records, attendance, exams, fees, library, and more—all in one place.", normal_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Key Features:", subheading_style))
    features = [
        "✓ Student & Teacher Management",
        "✓ Attendance Tracking",
        "✓ Exam & Result Management",
        "✓ Fee Collection & Tracking",
        "✓ Library Management",
        "✓ Transport Tracking",
        "✓ Dormitory Management",
        "✓ Announcements & Messaging",
    ]
    for f in features:
        elements.append(Paragraph(f, bullet_style))
    elements.append(PageBreak())

    # Section 2: Getting Started
    elements.append(Paragraph("2. Getting Started", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("2.1 Login", subheading_style))
    elements.append(Paragraph("1. Open your browser and go to the school website", bullet_style))
    elements.append(Paragraph("2. Enter your username and password", bullet_style))
    elements.append(Paragraph("3. Click 'Sign In' button", bullet_style))
    elements.append(Paragraph("4. You will be redirected to your dashboard", bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("2.2 Default Credentials", subheading_style))
    cred_data = [
        ["Role", "Username", "Password"],
        ["Admin", "admin", "admin123"],
        ["Teacher", "teacher", "teacher123"],
        ["Student", "student", "student123"],
    ]
    t = Table(cred_data, colWidths=[1.5*inch, 2*inch, 2*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("⚠️ Important: Change your password after first login!", normal_style))
    elements.append(PageBreak())

    # Section 3: User Roles
    elements.append(Paragraph("3. User Roles", heading_style))
    elements.append(Spacer(1, 10))
    roles_data = [
        ["Role", "Access Level"],
        ["Admin", "Full access to all features and settings"],
        ["Teacher", "Manage classes, attendance, exams, results"],
        ["Student", "View results, attendance, timetable, fees"],
        ["Parent", "View ward's progress and fees"],
    ]
    t = Table(roles_data, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00897b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Section 4: Admin Dashboard
    elements.append(Paragraph("4. Admin Dashboard", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("The admin dashboard provides a complete overview of the school. It shows:", normal_style))
    admin_features = [
        "📊 Total Students, Teachers, Classes count",
        "💰 Fee Collections (Total & Monthly)",
        "📅 Today's Attendance",
        "📝 Upcoming Exams",
        "🔔 Recent Announcements",
        "📚 Quick Action Buttons",
    ]
    for f in admin_features:
        elements.append(Paragraph(f, bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("4.1 Quick Actions", subheading_style))
    elements.append(Paragraph("The Quick Actions grid provides one-click access to:", normal_style))
    actions = [
        "Add Student - Register new students",
        "Add Teacher - Create teacher accounts",
        "Add Class - Create new classes",
        "Assign Fees - Generate fee invoices",
        "Mark Attendance - Daily attendance",
        "Record Payment - Collect fees",
        "Announcement - Send notices",
        "Settings - System configuration",
    ]
    for a in actions:
        elements.append(Paragraph(a, bullet_style))
    elements.append(PageBreak())

    # Section 5: Student Management
    elements.append(Paragraph("5. Student Management", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("5.1 Adding a Student", subheading_style))
    steps = [
        "Go to Students → Student List",
        "Click 'Add Student' button",
        "Fill in required fields: First Name, Last Name, Email",
        "Enter Student ID (auto-generated if left blank)",
        "Select Class from dropdown",
        "Fill Guardian details (Name, Phone, Relation)",
        "Click 'Save' button",
    ]
    for i, s in enumerate(steps, 1):
        elements.append(Paragraph(f"{i}. {s}", bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("5.2 Student Fields", subheading_style))
    fields = [
        ["Field", "Description"],
        ["Student ID", "Unique identifier (auto-generated)"],
        ["First/Last Name", " Student's full name"],
        ["Email", "Contact email address"],
        ["Current Class", "Assigned class"],
        ["Roll Number", "Class roll number"],
        ["Guardian Name", "Parent/guardian full name"],
        ["Guardian Phone", "Contact number"],
        ["Guardian Relation", "Father/Mother/Other"],
    ]
    t = Table(fields, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Section 6: Teacher Management
    elements.append(Paragraph("6. Teacher Management", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Adding teachers: Go to Teachers → Add Teacher", normal_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Teacher Information:", subheading_style))
    t_info = [
        ["Field", "Description"],
        ["Employee ID", "Unique staff identifier"],
        ["First/Last Name", "Teacher's full name"],
        ["Email", "Contact email"],
        ["Phone", "Contact number"],
        ["Subjects", "Subjects to teach"],
        ["Classes", "Classes to handle"],
    ]
    t = Table(t_info, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00897b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Section 7: Attendance
    elements.append(Paragraph("7. Attendance", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("7.1 Bulk Attendance", subheading_style))
    elements.append(Paragraph("To mark attendance for an entire class:", normal_style))
    att_steps = [
        "Go to Attendance → Mark Attendance",
        "Select Class from dropdown",
        "Choose Date",
        "Mark each student as Present/Absent/Late",
        "Add remarks if needed",
        "Click 'Save Attendance'",
    ]
    for s in att_steps:
        elements.append(Paragraph(s, bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("7.2 Attendance Status", subheading_style))
    status = [
        ["Status", "Description"],
        ["Present", "Student was in class"],
        ["Absent", "Student was absent"],
        ["Late", "Student arrived late"],
        ["Excused", "Absence with approval"],
    ]
    t = Table(status, colWidths=[1.5*inch, 3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ff8f00")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Section 8: Exams & Results
    elements.append(Paragraph("8. Exams & Results", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("8.1 Create Exam", subheading_style))
    exam_steps = [
        "Go to Academics → Exams",
        "Click 'Add Exam'",
        "Enter Exam Name (e.g., Mid-Term 2024)",
        "Select Exam Type (Termly/Unit Test/Quiz)",
        "Choose Academic Year",
        "Set Start & End Dates",
        "Click 'Save'",
    ]
    for s in exam_steps:
        elements.append(Paragraph(s, bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("8.2 Enter Results", subheading_style))
    result_steps = [
        "Go to Academics → Results",
        "Click 'Add Result'",
        "Select Student",
        "Select Exam Schedule",
        "Enter Marks Obtained",
        "Add remarks (optional)",
        "Click 'Save'",
    ]
    for s in result_steps:
        elements.append(Paragraph(s, bullet_style))
    elements.append(PageBreak())

    # Section 9: Fee Management
    elements.append(Paragraph("9. Fee Management", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("9.1 Fee Workflow", subheading_style))
    fee_steps = [
        "1. Create Fee Categories (Tuition, Transport, Library, etc.)",
        "2. Create Fee Particulars (specific fee items)",
        "3. Assign Fees to Students",
        "4. Students/Parents view fees",
        "5. Record Payments",
        "6. Track pending dues",
    ]
    for s in fee_steps:
        elements.append(Paragraph(s, bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("9.2 Fee Status", subheading_style))
    fee_status = [
        ["Status", "Meaning"],
        ["Pending", "Fee assigned, not paid"],
        ["Partial", "Partial payment received"],
        ["Paid", "Full payment received"],
        ["Overdue", "Payment past due date"],
    ]
    t = Table(fee_status, colWidths=[1.5*inch, 3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d32f2f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Section 10: Library
    elements.append(Paragraph("10. Library Management", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("10.1 Adding Books", subheading_style))
    elements.append(Paragraph("Go to Library → Books → Add Book", normal_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("10.2 Issue Book", subheading_style))
    elements.append(Paragraph("Library → Issue Book → Select Member, Book, Due Date → Save", normal_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("10.3 Return Book", subheading_style))
    elements.append(Paragraph("Library → Issue/Return → Mark as Returned", normal_style))
    elements.append(PageBreak())

    # Section 11: Communication
    elements.append(Paragraph("11. Communication", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("11.1 Announcements", subheading_style))
    elements.append(Paragraph("Create public announcements:", normal_style))
    anc_steps = [
        "Go to Communication → Announcements",
        "Click 'Add Announcement'",
        "Enter Title and Content",
        "Select Target Roles (All/Teachers/Students/Parents)",
        "Set Active status",
        "Click 'Save'",
    ]
    for s in anc_steps:
        elements.append(Paragraph(s, bullet_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("11.2 Private Messages", subheading_style))
    elements.append(Paragraph("Send direct messages to individuals or groups", normal_style))
    elements.append(PageBreak())

    # Keyboard Shortcuts
    elements.append(Paragraph("Keyboard Shortcuts", heading_style))
    elements.append(Spacer(1, 10))
    shortcuts = [
        ["Shortcut", "Action"],
        ["⌘ + K", "Open Global Search"],
        ["Ctrl + S", "Save current form"],
        ["Esc", "Close modal/Cancel"],
    ]
    t = Table(shortcuts, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7b1fa2")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Troubleshooting
    elements.append(Paragraph("Troubleshooting", heading_style))
    elements.append(Spacer(1, 10))
    issues = [
        ["Issue", "Solution"],
        ["Can't login", "Check credentials or reset password"],
        ["Page not loading", "Clear browser cache or try another browser"],
        ["Data not saving", "Fill all required fields"],
        ["Slow performance", "Check internet connection"],
    ]
    t = Table(issues, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d32f2f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 30))

    # Footer
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, alignment=TA_CENTER, textColor=colors.grey)
    elements.append(Paragraph("-" * 50, footer_style))
    elements.append(Paragraph(f"School Management System User Manual | © {datetime.now().year} SchoolMS", footer_style))
    elements.append(Paragraph("For support: support@schoolms.com", footer_style))

    doc.build(elements)
    buffer.close()
    print("User manual created: SchoolMS_User_Manual.pdf")


if __name__ == "__main__":
    generate_user_manual()