from rest_framework import serializers, viewsets
from .models import Dormitory, Room, StudentRoom


class DormitorySerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    occupied_beds = serializers.IntegerField(source="get_occupied_beds", read_only=True)

    class Meta:
        model = Dormitory
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    dormitory_name = serializers.CharField(source="dormitory.name", read_only=True)
    room_type_display = serializers.CharField(
        source="get_room_type_display", read_only=True
    )
    available_beds = serializers.IntegerField(
        source="get_available_beds", read_only=True
    )

    class Meta:
        model = Room
        fields = "__all__"


class StudentRoomSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name", read_only=True
    )
    student_id = serializers.CharField(source="student.student_id", read_only=True)
    room_number = serializers.CharField(source="room.room_number", read_only=True)
    dormitory_name = serializers.CharField(source="room.dormitory.name", read_only=True)

    class Meta:
        model = StudentRoom
        fields = "__all__"


class DormitoryViewSet(viewsets.ModelViewSet):
    queryset = Dormitory.objects.all()
    serializer_class = DormitorySerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related("dormitory").all()
    serializer_class = RoomSerializer


class StudentRoomViewSet(viewsets.ModelViewSet):
    queryset = StudentRoom.objects.select_related(
        "student", "student__user", "room", "room__dormitory"
    ).all()
    serializer_class = StudentRoomSerializer
