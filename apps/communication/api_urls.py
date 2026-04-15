from rest_framework.routers import DefaultRouter
from .serializers import (
    AnnouncementViewSet,
    MessageViewSet,
    NotificationViewSet,
    ContactViewSet,
)

router = DefaultRouter()
router.register(r"announcements", AnnouncementViewSet, basename="announcement")
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"contacts", ContactViewSet, basename="contact")

urlpatterns = []
