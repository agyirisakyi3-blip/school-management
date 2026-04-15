from rest_framework.routers import DefaultRouter
from .serializers import (
    FeeCategoryViewSet,
    FeeStructureViewSet,
    StudentFeeViewSet,
    PaymentViewSet,
    ExpenseViewSet,
)

router = DefaultRouter()
router.register(r"fee-categories", FeeCategoryViewSet, basename="fee-category")
router.register(r"fee-structures", FeeStructureViewSet, basename="fee-structure")
router.register(r"student-fees", StudentFeeViewSet, basename="student-fee")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"expenses", ExpenseViewSet, basename="expense")

urlpatterns = []
