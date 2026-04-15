from django.contrib import admin
from .models import Student, Class, Subject, AcademicYear


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "is_current"]
    list_filter = ["is_current"]
    search_fields = ["name"]


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "academic_year", "class_teacher"]
    list_filter = ["academic_year"]
    search_fields = ["name", "code"]
    autocomplete_fields = ["class_teacher"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    search_fields = ["name", "code"]
    filter_horizontal = ["classes"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["student_id", "user", "current_class", "guardian_name", "is_active"]
    list_filter = ["current_class", "is_active", "admission_date"]
    search_fields = [
        "student_id",
        "user__first_name",
        "user__last_name",
        "guardian_name",
    ]
    autocomplete_fields = ["user", "current_class"]
    readonly_fields = ["created_at", "updated_at"]
