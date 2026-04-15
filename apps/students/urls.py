from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "students"

urlpatterns = [
    path("", views.StudentListView.as_view(), name="student_list"),
    path(
        "bulk-action/",
        views.StudentBulkActionView.as_view(),
        name="student_bulk_action",
    ),
    path("create/", views.StudentCreateView.as_view(), name="student_create"),
    path("<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path(
        "<int:pk>/update/",
        views.StudentUpdateView.as_view(),
        name="student_update",
    ),
    path(
        "<int:pk>/delete/",
        views.StudentDeleteView.as_view(),
        name="student_delete",
    ),
    path("classes/", views.ClassListView.as_view(), name="class_list"),
    path("classes/create/", views.ClassCreateView.as_view(), name="class_create"),
    path("classes/<int:pk>/", views.ClassDetailView.as_view(), name="class_detail"),
    path(
        "classes/<int:pk>/update/", views.ClassUpdateView.as_view(), name="class_update"
    ),
    path(
        "classes/<int:pk>/delete/", views.ClassDeleteView.as_view(), name="class_delete"
    ),
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/create/", views.SubjectCreateView.as_view(), name="subject_create"),
    path(
        "subjects/<int:pk>/update/",
        views.SubjectUpdateView.as_view(),
        name="subject_update",
    ),
    path(
        "academic-years/",
        views.AcademicYearListView.as_view(),
        name="academic_year_list",
    ),
    path(
        "academic-years/create/",
        views.AcademicYearCreateView.as_view(),
        name="academic_year_create",
    ),
]
