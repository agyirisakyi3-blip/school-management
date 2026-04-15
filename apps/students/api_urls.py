from rest_framework.routers import DefaultRouter
from .serializers import (
    StudentViewSet,
    ClassViewSet,
    SubjectViewSet,
    AcademicYearViewSet,
)

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"classes", ClassViewSet, basename="class")
router.register(r"subjects", SubjectViewSet, basename="subject")
router.register(r"academic-years", AcademicYearViewSet, basename="academic-year")

urlpatterns = []
