from rest_framework.routers import DefaultRouter
from .api import HomeworkViewSet, HomeworkSubmissionViewSet

router = DefaultRouter()
router.register(r"homeworks", HomeworkViewSet)
router.register(r"submissions", HomeworkSubmissionViewSet)

urlpatterns = router.urls
