from rest_framework.routers import DefaultRouter
from .serializers import TeacherViewSet, TeacherSubjectViewSet

router = DefaultRouter()
router.register(r"teachers", TeacherViewSet, basename="teacher")
router.register(r"teacher-subjects", TeacherSubjectViewSet, basename="teacher-subject")

urlpatterns = []
