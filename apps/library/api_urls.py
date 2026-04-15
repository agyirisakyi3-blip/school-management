from rest_framework.routers import DefaultRouter
from .serializers import (
    BookViewSet,
    BookCategoryViewSet,
    LibraryMemberViewSet,
    BookIssueViewSet,
)

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"categories", BookCategoryViewSet)
router.register(r"members", LibraryMemberViewSet)
router.register(r"issues", BookIssueViewSet)

urlpatterns = router.urls
