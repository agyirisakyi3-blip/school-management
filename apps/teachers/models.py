from django.db import models
from django.conf import settings


class Teacher(models.Model):
    """Teacher profile model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    employee_id = models.CharField(max_length=20, unique=True)
    join_date = models.DateField()
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class TeacherSubject(models.Model):
    """Assignment of subjects to teachers."""

    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="teacher_subjects"
    )
    subject = models.ForeignKey(
        "students.Subject", on_delete=models.CASCADE, related_name="subject_teachers"
    )
    assigned_class = models.ForeignKey(
        "students.Class", on_delete=models.CASCADE, related_name="class_teachers"
    )
    academic_year = models.ForeignKey(
        "students.AcademicYear", on_delete=models.CASCADE, related_name="year_teachers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Teacher Subject Assignment"
        verbose_name_plural = "Teacher Subject Assignments"
        unique_together = ["teacher", "subject", "assigned_class", "academic_year"]

    def __str__(self):
        return f"{self.teacher} - {self.subject} ({self.assigned_class})"
