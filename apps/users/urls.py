from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path("api/search/", views.api_search, name="api_search"),
    path("api/notifications/", views.api_notifications, name="api_notifications"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/admin/", views.AdminDashboardView.as_view(), name="admin_dashboard"
    ),
    path(
        "dashboard/teacher/",
        views.TeacherDashboardView.as_view(),
        name="teacher_dashboard",
    ),
    path(
        "dashboard/student/",
        views.StudentDashboardView.as_view(),
        name="student_dashboard",
    ),
    path(
        "dashboard/parent/",
        views.ParentDashboardView.as_view(),
        name="parent_dashboard",
    ),
    # Admin Control Panel
    path(
        "admin-panel/",
        views.AdminControlPanelView.as_view(),
        name="admin_control_panel",
    ),
    # User Management
    path(
        "admin-panel/users/",
        views.UserManagementListView.as_view(),
        name="user_management",
    ),
    path(
        "admin-panel/users/create/",
        views.UserCreateView.as_view(),
        name="user_create",
    ),
    path(
        "admin-panel/users/<int:pk>/edit/",
        views.UserEditView.as_view(),
        name="user_edit",
    ),
    path(
        "admin-panel/users/<int:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="user_delete",
    ),
    path(
        "admin-panel/users/<int:pk>/toggle-active/",
        views.toggle_user_active,
        name="user_toggle_active",
    ),
    path(
        "admin-panel/users/<int:pk>/reset-password/",
        views.reset_user_password,
        name="user_reset_password",
    ),
    # Activity Logs
    path(
        "admin-panel/activity-logs/",
        views.ActivityLogListView.as_view(),
        name="activity_logs",
    ),
    # User Profile
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    # Non-Teaching Staff
    path("staff/", views.NonTeachingStaffListView.as_view(), name="staff_list"),
    path(
        "staff/create/", views.NonTeachingStaffCreateView.as_view(), name="staff_create"
    ),
    path(
        "staff/<int:pk>/",
        views.NonTeachingStaffDetailView.as_view(),
        name="staff_detail",
    ),
    path(
        "staff/<int:pk>/edit/",
        views.NonTeachingStaffUpdateView.as_view(),
        name="staff_update",
    ),
]
