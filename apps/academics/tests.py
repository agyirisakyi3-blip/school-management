import pytest
from datetime import date, time
from django.contrib.auth import get_user_model
from apps.students.models import AcademicYear, Class, Subject, Student
from apps.academics.models import Attendance, Exam, ExamSchedule, Result

User = get_user_model()


@pytest.mark.django_db
class TestAttendanceModel:
    def test_attendance_str(self):
        user = User.objects.create_user(username="attuser", email="att@test.com", password="test123")
        ay = AcademicYear.objects.create(name="2024", start_date=date(2024, 1, 1), end_date=date(2024, 12, 31))
        cls = Class.objects.create(name="Form 1", code="F1", academic_year=ay)
        student = Student.objects.create(
            user=user,
            student_id="ST001",
            admission_date=date(2024, 1, 1),
            current_class=cls,
            guardian_name="Parent",
            guardian_phone="1234567890",
            guardian_relation="Father"
        )
        attendance = Attendance.objects.create(
            student=student,
            date=date(2024, 1, 15),
            status=Attendance.Status.PRESENT
        )
        assert str(attendance) == f"{student} - 2024-01-15 - Present"


@pytest.mark.django_db
class TestExamModel:
    def test_exam_str(self):
        user = User.objects.create_user(username="examuser", email="exam@test.com", password="test123")
        ay = AcademicYear.objects.create(name="2024", start_date=date(2024, 1, 1), end_date=date(2024, 12, 31))
        exam = Exam.objects.create(
            name="Mid Term",
            exam_type="Termly",
            academic_year=ay,
            start_date=date(2024, 4, 1),
            end_date=date(2024, 4, 15)
        )
        assert str(exam) == "Mid Term (2024)"


@pytest.mark.django_db
class TestResultModel:
    def test_result_percentage(self):
        user = User.objects.create_user(username="resuser", email="res@test.com", password="test123")
        ay = AcademicYear.objects.create(name="2024", start_date=date(2024, 1, 1), end_date=date(2024, 12, 31))
        cls = Class.objects.create(name="Form 1", code="F1", academic_year=ay)
        subj = Subject.objects.create(name="Mathematics", code="MATH")
        subj.classes.add(cls)
        student = Student.objects.create(
            user=user,
            student_id="ST001",
            admission_date=date(2024, 1, 1),
            current_class=cls,
            guardian_name="Parent",
            guardian_phone="1234567890",
            guardian_relation="Father"
        )
        exam = Exam.objects.create(
            name="Mid Term",
            exam_type="Termly",
            academic_year=ay,
            start_date=date(2024, 4, 1),
            end_date=date(2024, 4, 15)
        )
        schedule = ExamSchedule.objects.create(
            exam=exam,
            subject=subj,
            assigned_class=cls,
            exam_date=date(2024, 4, 5),
            start_time=time(9, 0),
            end_time=time(11, 0),
            total_marks=100,
            passing_marks=40
        )
        result = Result.objects.create(
            student=student,
            exam_schedule=schedule,
            marks_obtained=75
        )
        assert result.percentage == 75.0

    def test_result_is_passed(self):
        user = User.objects.create_user(username="resuser2", email="res2@test.com", password="test123")
        ay = AcademicYear.objects.create(name="2024", start_date=date(2024, 1, 1), end_date=date(2024, 12, 31))
        cls = Class.objects.create(name="Form 1", code="F1", academic_year=ay)
        subj = Subject.objects.create(name="Science", code="SCI")
        subj.classes.add(cls)
        student = Student.objects.create(
            user=user,
            student_id="ST002",
            admission_date=date(2024, 1, 1),
            current_class=cls,
            guardian_name="Parent",
            guardian_phone="1234567890",
            guardian_relation="Father"
        )
        exam = Exam.objects.create(
            name="Mid Term",
            exam_type="Termly",
            academic_year=ay,
            start_date=date(2024, 4, 1),
            end_date=date(2024, 4, 15)
        )
        schedule = ExamSchedule.objects.create(
            exam=exam,
            subject=subj,
            assigned_class=cls,
            exam_date=date(2024, 4, 5),
            start_time=time(9, 0),
            end_time=time(11, 0),
            total_marks=100,
            passing_marks=40
        )
        result_pass = Result.objects.create(
            student=student,
            exam_schedule=schedule,
            marks_obtained=50
        )
        assert result_pass.is_passed is True
        assert result_pass.percentage == 50.0