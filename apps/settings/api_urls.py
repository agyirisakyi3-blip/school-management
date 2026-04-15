from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register("school-info", api.SchoolInfoViewSet, basename="school-info")
router.register(
    "general-settings", api.GeneralSettingsViewSet, basename="general-settings"
)
router.register("email-settings", api.EmailSettingsViewSet, basename="email-settings")
router.register("theme-settings", api.ThemeSettingsViewSet, basename="theme-settings")
router.register(
    "attendance-settings", api.AttendanceSettingsViewSet, basename="attendance-settings"
)
router.register(
    "result-settings", api.ResultSettingsViewSet, basename="result-settings"
)
router.register("fee-settings", api.FeeSettingsViewSet, basename="fee-settings")

urlpatterns = [
    path("", include(router.urls)),
]
