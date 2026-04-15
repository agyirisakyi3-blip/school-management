from django.db import models


class Dormitory(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=[
            ("boys", "Boys"),
            ("girls", "Girls"),
            ("mixed", "Mixed"),
        ],
        default="mixed",
    )
    address = models.TextField(blank=True)
    warden_name = models.CharField(max_length=100, blank=True)
    warden_phone = models.CharField(max_length=20, blank=True)
    total_rooms = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dormitory"
        verbose_name_plural = "Dormitories"

    def __str__(self):
        return self.name

    def get_occupied_rooms(self):
        return self.rooms.filter(studentroom__is_active=True).distinct().count()

    def get_occupied_beds(self):
        return StudentRoom.objects.filter(room__dormitory=self, is_active=True).count()


class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = "single", "Single"
        DOUBLE = "double", "Double"
        TRIPLE = "triple", "Triple"
        DORMITORY = "dormitory", "Dormitory"

    dormitory = models.ForeignKey(
        Dormitory,
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=RoomType.choices)
    floor = models.PositiveIntegerField(default=1)
    total_beds = models.PositiveIntegerField(default=1)
    cost_per_bed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        unique_together = ["dormitory", "room_number"]

    def __str__(self):
        return f"{self.dormitory.name} - Room {self.room_number}"

    def get_occupied_beds(self):
        return self.studentroom_set.filter(is_active=True).count()

    def get_available_beds(self):
        return self.total_beds - self.get_occupied_beds()


class StudentRoom(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="room_assignments",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="student_assignments",
    )
    bed_number = models.CharField(max_length=10, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Student Room"
        verbose_name_plural = "Student Rooms"

    def __str__(self):
        return f"{self.student} - {self.room}"
