from rest_framework import serializers, viewsets
from .models import Attendance, Exam, ExamSchedule, Result, Timetable


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name", read_only=True
    )

    class Meta:
        model = Attendance
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.CharField(
        source="academic_year.name", read_only=True
    )

    class Meta:
        model = Exam
        fields = "__all__"


class ExamScheduleSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source="exam.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    class_name = serializers.CharField(source="assigned_class.name", read_only=True)

    class Meta:
        model = ExamSchedule
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name", read_only=True
    )
    subject_name = serializers.CharField(
        source="exam_schedule.subject.name", read_only=True
    )
    percentage = serializers.ReadOnlyField()
    is_passed = serializers.ReadOnlyField()

    class Meta:
        model = Result
        fields = "__all__"


class TimetableSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="assigned_class.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(
        source="teacher.user.get_full_name", read_only=True
    )
    day_name = serializers.CharField(source="get_day_display", read_only=True)

    class Meta:
        model = Timetable
        fields = "__all__"


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class ExamScheduleViewSet(viewsets.ModelViewSet):
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
