from rest_framework import serializers, viewsets
from .models import FeeCategory, FeeStructure, StudentFee, Payment, Expense


class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = "__all__"


class FeeStructureSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    class_name = serializers.CharField(source="assigned_class.name", read_only=True)
    academic_year_name = serializers.CharField(
        source="academic_year.name", read_only=True
    )

    class Meta:
        model = FeeStructure
        fields = "__all__"


class StudentFeeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name", read_only=True
    )
    category_name = serializers.CharField(
        source="fee_structure.category.name", read_only=True
    )
    balance = serializers.ReadOnlyField()

    class Meta:
        model = StudentFee
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student_fee.student.user.get_full_name", read_only=True
    )
    received_by_name = serializers.CharField(
        source="received_by.get_full_name", read_only=True
    )

    class Meta:
        model = Payment
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    recorded_by_name = serializers.CharField(
        source="recorded_by.get_full_name", read_only=True
    )

    class Meta:
        model = Expense
        fields = "__all__"


class FeeCategoryViewSet(viewsets.ModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer


class StudentFeeViewSet(viewsets.ModelViewSet):
    queryset = StudentFee.objects.all()
    serializer_class = StudentFeeSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
