from django.db import models
from django.conf import settings


class Homework(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(
        "students.Subject",
        on_delete=models.CASCADE,
        related_name="homeworks",
    )
    class_obj = models.ForeignKey(
        "students.Class",
        on_delete=models.CASCADE,
        related_name="homeworks",
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_homeworks",
        limit_choices_to={"role": "teacher"},
    )
    due_date = models.DateTimeField()
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.MEDIUM
    )
    attachments = models.FileField(upload_to="homework/attachments/", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Homework"
        verbose_name_plural = "Homeworks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.class_obj.name}"

    def get_submission_count(self):
        return self.submissions.count()

    def get_accepted_count(self):
        return self.submissions.filter(status="accepted").count()


class HomeworkSubmission(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="homework_submissions",
    )
    submission_text = models.TextField(blank=True)
    attachment = models.FileField(upload_to="homework/submissions/", blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    feedback = models.TextField(blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Homework Submission"
        verbose_name_plural = "Homework Submissions"
        unique_together = ["homework", "student"]

    def __str__(self):
        return f"{self.student} - {self.homework.title}"
