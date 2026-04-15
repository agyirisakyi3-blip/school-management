from rest_framework import serializers, viewsets
from .models import LeaveType, LeaveRequest


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    leave_type_name = serializers.CharField(source="leave_type.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    total_days = serializers.IntegerField(source="get_total_days", read_only=True)

    class Meta:
        model = LeaveRequest
        fields = "__all__"


class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related(
        "user", "leave_type", "approved_by"
    ).all()
    serializer_class = LeaveRequestSerializer
