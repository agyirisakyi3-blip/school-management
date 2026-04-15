from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


def send_email(subject, message, recipient_list, html_message=None):
    """Send email to recipients."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def send_notification_email(user, subject, message):
    """Send notification email to a user."""
    if user.email:
        return send_email(
            subject=f"[SchoolMS] {subject}",
            message=message,
            recipient_list=[user.email],
        )
    return False


def send_announcement_email(announcement):
    """Send announcement email to all target users."""
    from apps.users.models import User
    from apps.students.models import Student

    target_role = announcement.target_roles
    recipients = []

    if target_role == "all":
        users = User.objects.filter(is_active=True)
    else:
        users = User.objects.filter(role=target_role, is_active=True)

    for user in users:
        if user.email:
            recipients.append(user.email)

    if recipients:
        return send_email(
            subject=announcement.title,
            message=announcement.content,
            recipient_list=recipients,
        )
    return False


def send_fee_reminder_email(student_fee):
    """Send fee reminder email to student's parent."""
    student = student_fee.student
    parent = student.parent

    if parent and parent.email:
        message = f"""
Dear {parent.get_full_name()},

This is a reminder that a fee payment is pending for your ward, {student.user.get_full_name()}.

Fee Details:
- Category: {student_fee.fee_structure.category.name}
- Amount Due: ${student_fee.balance}
- Due Date: {student_fee.due_date}

Please make the payment at the earliest to avoid any inconvenience.

Best regards,
School Management System
        """
        return send_email(
            subject=f"Fee Payment Reminder - {student.user.get_full_name()}",
            message=message,
            recipient_list=[parent.email],
        )
    return False


def send_attendance_notification_email(student, attendance):
    """Send attendance notification to parent."""
    parent = student.parent

    if parent and parent.email:
        status_text = "present" if attendance.status == "present" else "absent"
        message = f"""
Dear {parent.get_full_name()},

This is to inform you that your ward, {student.user.get_full_name()}, was marked as {status_text} on {attendance.date}.

{"Your child needs to improve attendance." if attendance.status == "absent" else "Great! Your child has maintained good attendance."}

Best regards,
School Management System
        """
        return send_email(
            subject=f"Attendance Update - {student.user.get_full_name()}",
            message=message,
            recipient_list=[parent.email],
        )
    return False


def send_exam_notification_email(exam):
    """Send exam schedule notification to students."""
    from apps.students.models import Student

    recipients = []
    students = Student.objects.filter(is_active=True)

    for student in students:
        if student.user.email:
            recipients.append(student.user.email)

    if recipients:
        message = f"""
Dear Student,

This is to inform you about an upcoming examination.

Exam Details:
- Name: {exam.name}
- Type: {exam.get_exam_type_display()}
- Start Date: {exam.start_date}
- End Date: {exam.end_date}

Please prepare accordingly.

Best regards,
School Management System
        """
        return send_email(
            subject=f"Upcoming Exam: {exam.name}",
            message=message,
            recipient_list=recipients,
        )
    return False
