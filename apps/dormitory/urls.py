from django.urls import path
from . import views

app_name = "dormitory"

urlpatterns = [
    path("", views.DormitoryDashboardView.as_view(), name="dashboard"),
    path("create/", views.DormitoryCreateView.as_view(), name="dormitory_create"),
    path(
        "<int:pk>/update/", views.DormitoryUpdateView.as_view(), name="dormitory_update"
    ),
    path(
        "<int:pk>/delete/", views.DormitoryDeleteView.as_view(), name="dormitory_delete"
    ),
    path("rooms/create/", views.RoomCreateView.as_view(), name="room_create"),
    path("rooms/<int:pk>/update/", views.RoomUpdateView.as_view(), name="room_update"),
    path("rooms/<int:pk>/delete/", views.RoomDeleteView.as_view(), name="room_delete"),
    path(
        "assignments/create/",
        views.StudentRoomCreateView.as_view(),
        name="assignment_create",
    ),
    path(
        "assignments/<int:pk>/delete/",
        views.StudentRoomDeleteView.as_view(),
        name="assignment_delete",
    ),
]
