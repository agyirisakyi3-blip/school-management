from rest_framework import serializers, viewsets
from .models import TransportRoute, Vehicle, VehicleRoute, StudentTransport


class TransportRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportRoute
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_type_display = serializers.CharField(
        source="get_vehicle_type_display", read_only=True
    )

    class Meta:
        model = Vehicle
        fields = "__all__"


class VehicleRouteSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source="route.name", read_only=True)
    vehicle_number = serializers.CharField(
        source="vehicle.vehicle_number", read_only=True
    )
    fare_amount = serializers.DecimalField(
        source="fare", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = VehicleRoute
        fields = "__all__"


class StudentTransportSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name", read_only=True
    )
    student_id = serializers.CharField(source="student.student_id", read_only=True)
    route_name = serializers.CharField(
        source="vehicle_route.route.name", read_only=True
    )
    vehicle_number = serializers.CharField(
        source="vehicle_route.vehicle.vehicle_number", read_only=True
    )

    class Meta:
        model = StudentTransport
        fields = "__all__"


class TransportRouteViewSet(viewsets.ModelViewSet):
    queryset = TransportRoute.objects.all()
    serializer_class = TransportRouteSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleRouteViewSet(viewsets.ModelViewSet):
    queryset = VehicleRoute.objects.select_related("route", "vehicle").all()
    serializer_class = VehicleRouteSerializer


class StudentTransportViewSet(viewsets.ModelViewSet):
    queryset = StudentTransport.objects.select_related(
        "student", "student__user", "vehicle_route", "vehicle_route__vehicle"
    ).all()
    serializer_class = StudentTransportSerializer
