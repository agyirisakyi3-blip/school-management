from rest_framework import serializers, viewsets
from .models import Teacher, TeacherSubject


class TeacherSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherSubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source="teacher.user.get_full_name", read_only=True
    )
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    class_name = serializers.CharField(source="assigned_class.name", read_only=True)
    academic_year_name = serializers.CharField(
        source="academic_year.name", read_only=True
    )

    class Meta:
        model = TeacherSubject
        fields = "__all__"


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer
