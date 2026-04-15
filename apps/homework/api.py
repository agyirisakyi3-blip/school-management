from rest_framework import serializers, viewsets
from .models import Homework, HomeworkSubmission


class HomeworkSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    class_name = serializers.CharField(source="class_obj.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.get_full_name", read_only=True)
    submission_count = serializers.IntegerField(
        source="get_submission_count", read_only=True
    )

    class Meta:
        model = Homework
        fields = "__all__"


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.user.get_full_name", read_only=True
    )
    student_id = serializers.CharField(source="student.student_id", read_only=True)
    homework_title = serializers.CharField(source="homework.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = HomeworkSubmission
        fields = "__all__"


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.select_related("subject", "class_obj", "teacher").all()
    serializer_class = HomeworkSerializer


class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
    queryset = HomeworkSubmission.objects.select_related(
        "homework", "student", "student__user"
    ).all()
    serializer_class = HomeworkSubmissionSerializer
