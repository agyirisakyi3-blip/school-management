from rest_framework.routers import DefaultRouter
from .api import DormitoryViewSet, RoomViewSet, StudentRoomViewSet

router = DefaultRouter()
router.register(r"dormitories", DormitoryViewSet)
router.register(r"rooms", RoomViewSet)
router.register(r"assignments", StudentRoomViewSet)

urlpatterns = router.urls
