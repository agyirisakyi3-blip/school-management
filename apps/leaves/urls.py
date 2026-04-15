from django.urls import path
from . import views

app_name = "leaves"

urlpatterns = [
    path("", views.LeaveDashboardView.as_view(), name="dashboard"),
    path("types/create/", views.LeaveTypeCreateView.as_view(), name="type_create"),
    path(
        "types/<int:pk>/update/",
        views.LeaveTypeUpdateView.as_view(),
        name="type_update",
    ),
    path(
        "types/<int:pk>/delete/",
        views.LeaveTypeDeleteView.as_view(),
        name="type_delete",
    ),
    path(
        "request/create/", views.LeaveRequestCreateView.as_view(), name="request_create"
    ),
    path(
        "request/<int:pk>/update/",
        views.LeaveRequestUpdateView.as_view(),
        name="request_update",
    ),
    path("request/<int:pk>/approve/", views.ApproveLeaveView.as_view(), name="approve"),
    path("request/<int:pk>/reject/", views.RejectLeaveView.as_view(), name="reject"),
    path("request/<int:pk>/cancel/", views.CancelLeaveView.as_view(), name="cancel"),
]
