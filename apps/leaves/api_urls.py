from rest_framework.routers import DefaultRouter
from .api import LeaveTypeViewSet, LeaveRequestViewSet

router = DefaultRouter()
router.register(r"types", LeaveTypeViewSet)
router.register(r"requests", LeaveRequestViewSet)

urlpatterns = router.urls
