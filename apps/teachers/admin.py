from django.contrib import admin
from .models import Teacher, TeacherSubject


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["employee_id", "user", "qualification", "department", "is_active"]
    list_filter = ["department", "is_active", "join_date"]
    search_fields = ["employee_id", "user__first_name", "user__last_name"]
    autocomplete_fields = ["user"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ["teacher", "subject", "assigned_class", "academic_year"]
    list_filter = ["academic_year", "assigned_class"]
    search_fields = [
        "teacher__user__first_name",
        "teacher__user__last_name",
        "subject__name",
    ]
    autocomplete_fields = ["teacher", "subject", "assigned_class", "academic_year"]
