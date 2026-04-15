from django.db import models
from django.conf import settings


class AcademicYear(models.Model):
    """Academic year model."""

    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class Class(models.Model):
    """Class/Grade model."""

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name="classes"
    )
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="class_teacher_of",
        limit_choices_to={"role": "teacher"},
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(models.Model):
    """Subject model."""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    classes = models.ManyToManyField(Class, related_name="subjects", blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    """Student profile model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    student_id = models.CharField(max_length=20, unique=True)
    admission_date = models.DateField()
    current_class = models.ForeignKey(
        Class, on_delete=models.SET_NULL, null=True, blank=True, related_name="students"
    )
    roll_number = models.CharField(max_length=20, blank=True)
    father_name = models.CharField(max_length=200, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)
    guardian_name = models.CharField(max_length=200)
    guardian_phone = models.CharField(max_length=20)
    guardian_relation = models.CharField(max_length=50)
    previous_school = models.CharField(max_length=200, blank=True)
    aadhar_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["user__first_name", "user__last_name"]


    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    @property
    def attendance_percentage(self):
        """Returns the attendance percentage for the student."""
        from ..academics.models import Attendance
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 0
        present = Attendance.objects.filter(student=self, status="present").count()
        return round((present / total) * 100, 1)

    @property
    def total_fees(self):
        """Returns the total fees allocated to the student."""
        from ..finance.models import StudentFee
        return StudentFee.objects.filter(student=self).aggregate(total=models.Sum("amount"))["total"] or 0

    @property
    def paid_fees(self):
        """Returns the total fees paid by the student."""
        from ..finance.models import StudentFee
        return StudentFee.objects.filter(student=self).aggregate(total=models.Sum("amount_paid"))["total"] or 0

    @property
    def fee_balance(self):
        """Returns the remaining fee balance."""
        return self.total_fees - self.paid_fees

    @property
    def fee_payment_percentage(self):
        """Returns the fee payment percentage."""
        total = self.total_fees
        if total == 0:
            return 100
        return round((self.paid_fees / total) * 100, 1)

    @property
    def average_score(self):
        """Returns the average score across all subjects."""
        from ..academics.models import Result
        results = Result.objects.filter(student=self)
        if not results.exists():
            return 0
        return round(results.aggregate(avg=models.Avg("marks_obtained"))["avg"], 1)
