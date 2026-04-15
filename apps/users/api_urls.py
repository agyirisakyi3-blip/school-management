from rest_framework.routers import DefaultRouter
from .serializers import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = []
