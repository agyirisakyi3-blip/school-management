from rest_framework.routers import DefaultRouter
from .api import (
    TransportRouteViewSet,
    VehicleViewSet,
    VehicleRouteViewSet,
    StudentTransportViewSet,
)

router = DefaultRouter()
router.register(r"routes", TransportRouteViewSet)
router.register(r"vehicles", VehicleViewSet)
router.register(r"assignments", VehicleRouteViewSet)
router.register(r"students", StudentTransportViewSet)

urlpatterns = router.urls
