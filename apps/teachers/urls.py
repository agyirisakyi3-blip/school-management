from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.TeacherListView.as_view(), name="teacher_list"),
    path("create/", views.TeacherCreateView.as_view(), name="teacher_create"),
    path("<int:pk>/", views.TeacherDetailView.as_view(), name="teacher_detail"),
    path(
        "<int:pk>/update/",
        views.TeacherUpdateView.as_view(),
        name="teacher_update",
    ),
    path(
        "<int:pk>/delete/",
        views.TeacherDeleteView.as_view(),
        name="teacher_delete",
    ),
    path(
        "subjects/", views.TeacherSubjectListView.as_view(), name="teacher_subject_list"
    ),
    path(
        "subjects/create/",
        views.TeacherSubjectCreateView.as_view(),
        name="teacher_subject_create",
    ),
]
