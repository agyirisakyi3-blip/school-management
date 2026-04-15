from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "academics"

urlpatterns = [
    path("", RedirectView.as_view(url="attendance/", permanent=False), name="index"),
    path("attendance/", views.AttendanceListView.as_view(), name="attendance_list"),
    path(
        "attendance/calendar/",
        views.AttendanceCalendarView.as_view(),
        name="attendance_calendar",
    ),
    path(
        "attendance/add/",
        views.AttendanceCreateView.as_view(),
        name="attendance_create",
    ),
    path(
        "attendance/bulk-add/",
        views.AttendanceBulkCreateView.as_view(),
        name="attendance_bulk_create",
    ),
    path("exams/", views.ExamListView.as_view(), name="exam_list"),
    path("exams/create/", views.ExamCreateView.as_view(), name="exam_create"),
    path("exams/<int:pk>/", views.ExamDetailView.as_view(), name="exam_detail"),
    path(
        "exams/schedule/add/",
        views.ExamScheduleCreateView.as_view(),
        name="exam_schedule_create",
    ),
    path("results/", views.ResultListView.as_view(), name="result_list"),
    path("results/add/", views.ResultCreateView.as_view(), name="result_create"),
    path("timetable/", views.TimetableListView.as_view(), name="timetable_list"),
    path(
        "timetable/add/", views.TimetableCreateView.as_view(), name="timetable_create"
    ),
    path("report/<int:pk>/", views.StudentReportView.as_view(), name="student_report"),
    path(
        "report/<int:pk>/pdf/",
        views.StudentReportPDFView.as_view(),
        name="student_report_pdf",
    ),
    # Online Exam URLs
    path("online-exams/", views.OnlineExamListView.as_view(), name="online_exam_list"),
    path("online-exams/<int:pk>/", views.OnlineExamView.as_view(), name="online_exam"),
    path(
        "online-exams/<int:pk>/result/",
        views.ExamResultView.as_view(),
        name="exam_result",
    ),
]
