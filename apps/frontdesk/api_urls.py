from rest_framework.routers import DefaultRouter
from .api import AdmissionQueryViewSet, VisitorViewSet, ComplaintViewSet

router = DefaultRouter()
router.register(r"queries", AdmissionQueryViewSet)
router.register(r"visitors", VisitorViewSet)
router.register(r"complaints", ComplaintViewSet)

urlpatterns = router.urls
