from django.db import models
from django.conf import settings


class TransportRoute(models.Model):
    name = models.CharField(max_length=100)
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transport Route"
        verbose_name_plural = "Transport Routes"

    def __str__(self):
        return f"{self.name} ({self.route_from} - {self.route_to})"


class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        BUS = "bus", "Bus"
        VAN = "van", "Van"
        MINIBUS = "minibus", "Minibus"
        CAR = "car", "Car"

    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices)
    model = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField()
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.vehicle_number} ({self.get_vehicle_type_display()})"


class VehicleRoute(models.Model):
    route = models.ForeignKey(
        TransportRoute, on_delete=models.CASCADE, related_name="vehicle_routes"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="route_assignments"
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehicle_routes",
        limit_choices_to={"role": "driver"},
    )
    pickup_time = models.TimeField(null=True, blank=True)
    drop_time = models.TimeField(null=True, blank=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vehicle Route"
        verbose_name_plural = "Vehicle Routes"

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.route.name}"


class StudentTransport(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="transport_assignments",
    )
    vehicle_route = models.ForeignKey(
        VehicleRoute, on_delete=models.CASCADE, related_name="assigned_students"
    )
    pickup_point = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    assigned_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Student Transport"
        verbose_name_plural = "Student Transports"
        unique_together = ["student", "vehicle_route"]

    def __str__(self):
        return f"{self.student} - {self.vehicle_route}"
