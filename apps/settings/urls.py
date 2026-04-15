from django.urls import path
from . import views

app_name = "settings"

urlpatterns = [
    path("", views.SettingsDashboardView.as_view(), name="dashboard"),
    path("school/", views.SchoolInfoUpdateView.as_view(), name="school_info"),
    path(
        "general/", views.GeneralSettingsUpdateView.as_view(), name="general_settings"
    ),
    path("email/", views.EmailSettingsUpdateView.as_view(), name="email_settings"),
    path("theme/", views.ThemeSettingsUpdateView.as_view(), name="theme_settings"),
    path(
        "attendance/",
        views.AttendanceSettingsUpdateView.as_view(),
        name="attendance_settings",
    ),
    path("results/", views.ResultSettingsUpdateView.as_view(), name="result_settings"),
    path("fees/", views.FeeSettingsUpdateView.as_view(), name="fee_settings"),
]
