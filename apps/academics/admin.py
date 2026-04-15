from django.contrib import admin
from .models import (
    Attendance,
    Exam,
    ExamSchedule,
    Result,
    Timetable,
    Question,
    StudentExam,
    StudentAnswer,
)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["student", "date", "status", "marked_by"]
    list_filter = ["date", "status"]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__student_id",
    ]
    date_hierarchy = "date"


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "exam_type",
        "academic_year",
        "start_date",
        "end_date",
        "is_active",
    ]
    list_filter = ["exam_type", "academic_year", "is_active"]
    search_fields = ["name"]


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "exam",
        "subject",
        "assigned_class",
        "exam_date",
        "start_time",
        "total_marks",
        "is_online",
    ]
    list_filter = ["exam", "assigned_class", "exam_date", "is_online"]
    search_fields = ["subject__name", "assigned_class__name"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["exam_schedule", "order", "question_type", "marks"]
    list_filter = ["exam_schedule__exam", "question_type"]
    search_fields = ["question_text"]


@admin.register(StudentExam)
class StudentExamAdmin(admin.ModelAdmin):
    list_display = ["student", "exam_schedule", "started_at", "is_submitted", "score"]
    list_filter = ["exam_schedule__exam", "is_submitted"]
    search_fields = ["student__user__first_name", "student__user__last_name"]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ["student_exam", "question", "is_correct"]
    list_filter = ["is_correct"]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ["student", "exam_schedule", "marks_obtained", "created_by"]
    list_filter = ["exam_schedule__exam", "exam_schedule__assigned_class"]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__student_id",
    ]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = [
        "assigned_class",
        "subject",
        "day",
        "start_time",
        "end_time",
        "teacher",
    ]
    list_filter = ["assigned_class", "day", "academic_year"]
    search_fields = ["subject__name", "assigned_class__name"]
