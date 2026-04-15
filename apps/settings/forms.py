from django import forms
from .models import (
    SchoolInfo,
    GeneralSettings,
    EmailSettings,
    ThemeSettings,
    AttendanceSettings,
    ResultSettings,
    FeeSettings,
)


class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = [
            "name",
            "tagline",
            "logo",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "phone",
            "mobile",
            "email",
            "website",
            "established_date",
            "registration_number",
            "tax_id",
        ]
        widgets = {
            "established_date": forms.DateInput(attrs={"type": "date"}),
            "logo": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["logo", "established_date"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class GeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = [
            "date_format",
            "time_format",
            "timezone",
            "currency",
            "currency_symbol",
            "decimal_places",
            "working_days",
            "class_duration",
            "break_duration",
            "school_start_time",
            "school_end_time",
            "require_student_photo",
            "require_guardian_info",
            "auto_assign_roll_number",
            "student_id_prefix",
            "teacher_id_prefix",
            "staff_id_prefix",
            "academic_year_start_month",
            "enable_sms",
            "enable_notifications",
            "enable_parent_portal",
        ]
        widgets = {
            "school_start_time": forms.TimeInput(attrs={"type": "time"}),
            "school_end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget_class = self.fields[field].widget.__class__.__name__
            if widget_class in ["Select", "TextInput", "TimeInput", "NumberInput"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})
            elif widget_class == "CheckboxInput":
                self.fields[field].widget.attrs.update({"class": "form-check-input"})


class EmailSettingsForm(forms.ModelForm):
    email_host_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
    )

    class Meta:
        model = EmailSettings
        fields = [
            "email_backend",
            "email_host",
            "email_port",
            "email_use_tls",
            "email_use_ssl",
            "email_host_user",
            "email_host_password",
            "email_from_name",
            "email_from_address",
            "email_signature",
            "test_email_recipient",
        ]
        widgets = {
            "email_signature": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget_class = self.fields[field].widget.__class__.__name__
            if widget_class in ["Select", "TextInput", "NumberInput", "EmailInput"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})
            elif widget_class == "CheckboxInput":
                self.fields[field].widget.attrs.update({"class": "form-check-input"})


class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = ThemeSettings
        fields = [
            "theme",
            "layout",
            "primary_color",
            "sidebar_color",
            "compact_mode",
            "box_shadow",
            "border_radius",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget_class = self.fields[field].widget.__class__.__name__
            if widget_class == "Select":
                self.fields[field].widget.attrs.update({"class": "form-select"})
            elif widget_class == "CheckboxInput":
                self.fields[field].widget.attrs.update({"class": "form-check-input"})


class AttendanceSettingsForm(forms.ModelForm):
    class Meta:
        model = AttendanceSettings
        fields = [
            "auto_absent_threshold",
            "require_attendance_remark",
            "allow_attendance_edit",
            "attendance_edit_days_limit",
            "attendance_percentage_required",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget_class = self.fields[field].widget.__class__.__name__
            if widget_class in ["Select", "NumberInput"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})
            elif widget_class == "CheckboxInput":
                self.fields[field].widget.attrs.update({"class": "form-check-input"})


class ResultSettingsForm(forms.ModelForm):
    class Meta:
        model = ResultSettings
        fields = [
            "grading_system",
            "publish_result",
            "require_attendance_for_result",
            "allow_rank",
            "show_pass_fail",
            "show_grade",
            "show_percentage",
            "show_remarks",
            "decimal_points",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget_class = self.fields[field].widget.__class__.__name__
            if widget_class in ["Select", "NumberInput"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})
            elif widget_class == "CheckboxInput":
                self.fields[field].widget.attrs.update({"class": "form-check-input"})


class FeeSettingsForm(forms.ModelForm):
    class Meta:
        model = FeeSettings
        fields = [
            "allow_partial_payment",
            "partial_payment_type",
            "partial_payment_amount",
            "late_fee_enabled",
            "late_fee_type",
            "late_fee_amount",
            "late_fee_after_days",
            "invoice_prefix",
            "due_warning_days",
            "auto_reminder",
        ]
        widgets = {
            "partial_payment_amount": forms.NumberInput(attrs={"step": "0.01"}),
            "late_fee_amount": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget_class = self.fields[field].widget.__class__.__name__
            if widget_class in ["Select", "TextInput", "NumberInput"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})
            elif widget_class == "CheckboxInput":
                self.fields[field].widget.attrs.update({"class": "form-check-input"})
