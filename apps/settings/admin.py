from django.contrib import admin
from .models import (
    SchoolInfo,
    GeneralSettings,
    EmailSettings,
    ThemeSettings,
    AttendanceSettings,
    ResultSettings,
    FeeSettings,
)


@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "city", "country"]
    search_fields = ["name", "email", "phone"]


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    list_display = ["currency", "timezone", "working_days"]


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ["email_host", "email_port", "email_from_address"]


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ["theme", "layout", "primary_color"]


@admin.register(AttendanceSettings)
class AttendanceSettingsAdmin(admin.ModelAdmin):
    list_display = ["auto_absent_threshold", "attendance_percentage_required"]


@admin.register(ResultSettings)
class ResultSettingsAdmin(admin.ModelAdmin):
    list_display = ["grading_system", "publish_result"]


@admin.register(FeeSettings)
class FeeSettingsAdmin(admin.ModelAdmin):
    list_display = ["allow_partial_payment", "late_fee_enabled", "invoice_prefix"]
