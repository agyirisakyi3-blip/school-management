from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SchoolInfo(models.Model):
    name = models.CharField(max_length=200, default="My School")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="school/logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="school/favicon/", blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "School Information"
        verbose_name_plural = "School Information"

    def __str__(self):
        return self.name

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class GeneralSettings(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GBP", "British Pound"),
        ("INR", "Indian Rupee"),
        ("PKR", "Pakistani Rupee"),
        ("BDT", "Bangladeshi Taka"),
        ("NGN", "Nigerian Naira"),
        ("KES", "Kenyan Shilling"),
        ("ZAR", "South African Rand"),
        ("PHP", "Philippine Peso"),
        ("MYR", "Malaysian Ringgit"),
        ("SGD", "Singapore Dollar"),
        ("GHS", "Ghana Cedis"),
        ("XOF", "CFA Franc (West Africa)"),
        ("XAF", "CFA Franc (Central Africa)"),
    ]

    TIMEZONE_CHOICES = [
        ("UTC", "UTC"),
        ("America/New_York", "Eastern Time (US)"),
        ("America/Chicago", "Central Time (US)"),
        ("America/Denver", "Mountain Time (US)"),
        ("America/Los_Angeles", "Pacific Time (US)"),
        ("Europe/London", "London"),
        ("Europe/Paris", "Paris"),
        ("Asia/Dubai", "Dubai"),
        ("Asia/Kolkata", "India"),
        ("Asia/Dhaka", "Bangladesh"),
        ("Asia/Karachi", "Pakistan"),
        ("Asia/Singapore", "Singapore"),
        ("Africa/Lagos", "Lagos"),
        ("Africa/Johannesburg", "Johannesburg"),
    ]

    date_format = models.CharField(max_length=20, default="Y-m-d")
    time_format = models.CharField(max_length=20, default="H:i")
    timezone = models.CharField(max_length=50, default="UTC", choices=TIMEZONE_CHOICES)
    currency = models.CharField(max_length=10, default="USD", choices=CURRENCY_CHOICES)
    currency_symbol = models.CharField(max_length=10, default="$")
    decimal_places = models.PositiveIntegerField(
        default=2, validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    working_days = models.CharField(
        max_length=50, default="Monday,Tuesday,Wednesday,Thursday,Friday"
    )
    class_duration = models.PositiveIntegerField(
        default=45, help_text="Duration in minutes"
    )
    break_duration = models.PositiveIntegerField(
        default=15, help_text="Break duration in minutes"
    )
    school_start_time = models.TimeField(default="08:00")
    school_end_time = models.TimeField(default="15:00")
    require_student_photo = models.BooleanField(default=True)
    require_guardian_info = models.BooleanField(default=True)
    auto_assign_roll_number = models.BooleanField(default=True)
    student_id_prefix = models.CharField(max_length=10, default="STU")
    teacher_id_prefix = models.CharField(max_length=10, default="TCH")
    staff_id_prefix = models.CharField(max_length=10, default="STF")
    academic_year_start_month = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    enable_sms = models.BooleanField(default=False)
    enable_notifications = models.BooleanField(default=True)
    enable_parent_portal = models.BooleanField(default=True)

    class Meta:
        verbose_name = "General Settings"
        verbose_name_plural = "General Settings"

    def __str__(self):
        return "General Settings"

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class EmailSettings(models.Model):
    EMAIL_BACKEND_CHOICES = [
        ("django.core.mail.backends.smtp.EmailBackend", "SMTP"),
        ("django.core.mail.backends.console.EmailBackend", "Console (Development)"),
        ("django.core.mail.backends.filebased.EmailBackend", "File (Development)"),
    ]

    email_backend = models.CharField(
        max_length=100,
        default="django.core.mail.backends.smtp.EmailBackend",
        choices=EMAIL_BACKEND_CHOICES,
    )
    email_host = models.CharField(max_length=200, blank=True)
    email_port = models.PositiveIntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_use_ssl = models.BooleanField(default=False)
    email_host_user = models.EmailField(blank=True)
    email_host_password = models.CharField(max_length=200, blank=True)
    email_from_name = models.CharField(max_length=100, default="School Management")
    email_from_address = models.EmailField(blank=True)
    email_signature = models.TextField(blank=True)
    test_email_recipient = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Email Settings"
        verbose_name_plural = "Email Settings"

    def __str__(self):
        return "Email Settings"

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class ThemeSettings(models.Model):
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("auto", "Auto (System)"),
    ]

    LAYOUT_CHOICES = [
        ("sidebar", "Sidebar (Traditional)"),
        ("collapsed", "Collapsed Sidebar"),
        ("horizontal", "Horizontal Menu"),
    ]

    PRIMARY_COLOR_CHOICES = [
        ("#0d6efd", "Blue"),
        ("#6610f2", "Purple"),
        ("#6f42c1", "Indigo"),
        ("#198754", "Green"),
        ("#20c997", "Teal"),
        ("#fd7e14", "Orange"),
        ("#dc3545", "Red"),
        ("#0dcaf0", "Cyan"),
    ]

    theme = models.CharField(max_length=20, default="light", choices=THEME_CHOICES)
    layout = models.CharField(max_length=20, default="sidebar", choices=LAYOUT_CHOICES)
    primary_color = models.CharField(max_length=20, default="#0d6efd")
    sidebar_color = models.CharField(max_length=20, default="#1e1e2d")
    compact_mode = models.BooleanField(default=False)
    box_shadow = models.BooleanField(default=True)
    border_radius = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Theme Settings"
        verbose_name_plural = "Theme Settings"

    def __str__(self):
        return "Theme Settings"

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class AttendanceSettings(models.Model):
    auto_absent_threshold = models.PositiveIntegerField(
        default=10,
        help_text="Days of consecutive absence before marking as auto-absent",
    )
    require_attendance_remark = models.BooleanField(default=False)
    allow_attendance_edit = models.BooleanField(default=True)
    attendance_edit_days_limit = models.PositiveIntegerField(
        default=7,
        help_text="Days limit for editing attendance (0 = no limit)",
    )
    attendance_percentage_required = models.PositiveIntegerField(
        default=75,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = "Attendance Settings"
        verbose_name_plural = "Attendance Settings"

    def __str__(self):
        return "Attendance Settings"

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class ResultSettings(models.Model):
    GRADING_SYSTEM_CHOICES = [
        ("percentage", "Percentage Based"),
        ("grade", "Grade Based"),
        ("gpa", "GPA Based"),
        ("cwa", "CWA Based"),
    ]

    RESULT_PUBLISH_AUTO = "auto"
    RESULT_PUBLISH_MANUAL = "manual"

    grading_system = models.CharField(
        max_length=20, default="percentage", choices=GRADING_SYSTEM_CHOICES
    )
    publish_result = models.CharField(
        max_length=20,
        default=RESULT_PUBLISH_MANUAL,
        choices=[(RESULT_PUBLISH_AUTO, "Automatic"), (RESULT_PUBLISH_MANUAL, "Manual")],
    )
    require_attendance_for_result = models.BooleanField(default=False)
    allow_rank = models.BooleanField(default=True)
    show_pass_fail = models.BooleanField(default=True)
    show_grade = models.BooleanField(default=True)
    show_percentage = models.BooleanField(default=True)
    show_remarks = models.BooleanField(default=True)
    decimal_points = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2)]
    )

    class Meta:
        verbose_name = "Result Settings"
        verbose_name_plural = "Result Settings"

    def __str__(self):
        return "Result Settings"

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class FeeSettings(models.Model):
    ALLOW_PARTIAL_PAYMENT_CHOICES = [
        ("full", "Full Payment Only"),
        ("percentage", "Percentage Based"),
        ("fixed", "Fixed Amount"),
    ]

    allow_partial_payment = models.BooleanField(default=True)
    partial_payment_type = models.CharField(
        max_length=20,
        default="percentage",
        choices=[
            ("percentage", "Percentage Based"),
            ("fixed", "Fixed Amount"),
        ],
    )
    partial_payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    late_fee_enabled = models.BooleanField(default=False)
    late_fee_type = models.CharField(
        max_length=20,
        default="percentage",
        choices=[
            ("percentage", "Percentage"),
            ("fixed", "Fixed Amount"),
        ],
    )
    late_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    late_fee_after_days = models.PositiveIntegerField(default=7)
    invoice_prefix = models.CharField(max_length=10, default="INV")
    due_warning_days = models.PositiveIntegerField(default=3)
    auto_reminder = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Fee Settings"
        verbose_name_plural = "Fee Settings"

    def __str__(self):
        return "Fee Settings"

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance
