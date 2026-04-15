from rest_framework import serializers, viewsets
from .models import Student, Class, Subject, AcademicYear


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(
        source="class_teacher.get_full_name", read_only=True
    )

    class Meta:
        model = Class
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class_names = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = "__all__"

    def get_class_names(self, obj):
        return [c.name for c in obj.classes.all()]


class StudentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    class_name = serializers.CharField(source="current_class.name", read_only=True)

    class Meta:
        model = Student
        fields = "__all__"


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return Student.objects.all()
        elif user.is_teacher:
            teacher_class = Class.objects.filter(class_teacher=user).first()
            if teacher_class:
                return Student.objects.filter(current_class=teacher_class)
            return Student.objects.none()
        elif user.is_student:
            return Student.objects.filter(user=user)
        return Student.objects.none()


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
