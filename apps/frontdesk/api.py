from rest_framework import serializers, viewsets
from .models import AdmissionQuery, Visitor, Complaint


class AdmissionQuerySerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="class_interested.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = AdmissionQuery
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


class ComplaintSerializer(serializers.ModelSerializer):
    complaint_type_display = serializers.CharField(
        source="get_complaint_type_display", read_only=True
    )
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Complaint
        fields = "__all__"


class AdmissionQueryViewSet(viewsets.ModelViewSet):
    queryset = AdmissionQuery.objects.select_related("class_interested").all()
    serializer_class = AdmissionQuerySerializer


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
