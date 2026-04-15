from django.urls import path
from . import views

app_name = "frontdesk"

urlpatterns = [
    path("", views.FrontdeskDashboardView.as_view(), name="dashboard"),
    path(
        "queries/create/", views.AdmissionQueryCreateView.as_view(), name="query_create"
    ),
    path(
        "queries/<int:pk>/update/",
        views.AdmissionQueryUpdateView.as_view(),
        name="query_update",
    ),
    path(
        "queries/<int:pk>/delete/",
        views.AdmissionQueryDeleteView.as_view(),
        name="query_delete",
    ),
    path("visitors/create/", views.VisitorCreateView.as_view(), name="visitor_create"),
    path(
        "visitors/<int:pk>/checkout/",
        views.VisitorCheckOutView.as_view(),
        name="visitor_checkout",
    ),
    path(
        "visitors/<int:pk>/delete/",
        views.VisitorDeleteView.as_view(),
        name="visitor_delete",
    ),
    path(
        "complaints/create/",
        views.ComplaintCreateView.as_view(),
        name="complaint_create",
    ),
    path(
        "complaints/<int:pk>/update/",
        views.ComplaintUpdateView.as_view(),
        name="complaint_update",
    ),
    path(
        "complaints/<int:pk>/delete/",
        views.ComplaintDeleteView.as_view(),
        name="complaint_delete",
    ),
]
