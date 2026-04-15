from django.urls import path
from . import views

app_name = "homework"

urlpatterns = [
    path("", views.HomeworkListView.as_view(), name="list"),
    path("create/", views.HomeworkCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.HomeworkUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.HomeworkDeleteView.as_view(), name="delete"),
    path("<int:pk>/submit/", views.HomeworkSubmissionView.as_view(), name="submit"),
    path(
        "<int:homework_id>/submissions/",
        views.SubmissionListView.as_view(),
        name="submissions",
    ),
    path(
        "submissions/<int:pk>/evaluate/",
        views.EvaluateSubmissionView.as_view(),
        name="evaluate",
    ),
]
