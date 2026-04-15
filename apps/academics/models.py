from django.db import models
from django.utils import timezone


class Attendance(models.Model):
    """Daily attendance model."""

    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        LATE = "late", "Late"
        EXCUSED = "excused", "Excused"

    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, related_name="attendances"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PRESENT
    )
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="marked_attendances",
    )

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        unique_together = ["student", "date"]

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"


class Exam(models.Model):
    """Exam model."""

    name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=50)
    academic_year = models.ForeignKey(
        "students.AcademicYear", on_delete=models.CASCADE, related_name="exams"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

    @property
    def is_online(self):
        """Check if exam has questions for online mode."""
        return hasattr(self, "questions") and self.questions.exists()


class ExamSchedule(models.Model):
    """Exam schedule model."""

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="exam_schedules"
    )
    subject = models.ForeignKey(
        "students.Subject", on_delete=models.CASCADE, related_name="exam_schedules"
    )
    assigned_class = models.ForeignKey(
        "students.Class", on_delete=models.CASCADE, related_name="exam_schedules"
    )
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    venue = models.CharField(max_length=200, blank=True)
    is_online = models.BooleanField(default=False, help_text="Enable online exam mode")
    duration_minutes = models.PositiveIntegerField(
        default=60, help_text="Duration for online exam in minutes"
    )

    class Meta:
        verbose_name = "Exam Schedule"
        verbose_name_plural = "Exam Schedules"
        ordering = ["exam_date", "start_time"]

    def __str__(self):
        return f"{self.exam} - {self.subject} ({self.assigned_class})"

    @property
    def is_available(self):
        """Check if exam is currently available."""
        now = timezone.now()
        exam_datetime = timezone.make_aware(
            timezone.datetime.combine(self.exam_date, self.start_time)
        )
        end_datetime = timezone.make_aware(
            timezone.datetime.combine(self.exam_date, self.end_time)
        )
        return (
            self.is_online
            and self.exam.is_active
            and exam_datetime <= now <= end_datetime
        )


class Question(models.Model):
    """Exam question model for online exams."""

    QUESTION_TYPES = [
        ("multiple_choice", "Multiple Choice"),
        ("true_false", "True/False"),
        ("short_answer", "Short Answer"),
        ("essay", "Essay"),
    ]

    exam_schedule = models.ForeignKey(
        ExamSchedule, on_delete=models.CASCADE, related_name="questions"
    )
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPES, default="multiple_choice"
    )
    marks = models.PositiveIntegerField(default=1)
    options = models.JSONField(
        default=dict, blank=True, help_text="Options for multiple choice as JSON"
    )
    correct_answer = models.TextField(
        blank=True, help_text="Correct answer or answer key"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."


class StudentExam(models.Model):
    """Track student's exam attempts."""

    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, related_name="exam_attempts"
    )
    exam_schedule = models.ForeignKey(
        ExamSchedule, on_delete=models.CASCADE, related_name="student_exams"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    class Meta:
        unique_together = ["student", "exam_schedule"]

    def __str__(self):
        return f"{self.student} - {self.exam_schedule}"

    @property
    def time_remaining(self):
        """Calculate remaining time in minutes."""
        if self.is_submitted:
            return 0
        duration = self.exam_schedule.duration_minutes
        elapsed = (timezone.now() - self.started_at).total_seconds() / 60
        remaining = duration - elapsed
        return max(0, int(remaining))


class StudentAnswer(models.Model):
    """Store student's answers for each question."""

    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="student_answers"
    )
    answer = models.TextField(blank=True)
    marks_obtained = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    is_correct = models.BooleanField(default=False)
    evaluated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["student_exam", "question"]

    def __str__(self):
        return f"{self.student_exam.student} - Q{self.question.order}"


class Result(models.Model):
    """Student exam results model."""

    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, related_name="results"
    )
    exam_schedule = models.ForeignKey(
        ExamSchedule, on_delete=models.CASCADE, related_name="results"
    )
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_results",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"
        unique_together = ["student", "exam_schedule"]

    def __str__(self):
        return f"{self.student} - {self.exam_schedule.subject} - {self.marks_obtained}"

    @property
    def percentage(self):
        if self.exam_schedule.total_marks > 0:
            return (self.marks_obtained / self.exam_schedule.total_marks) * 100
        return 0

    @property
    def is_passed(self):
        return self.marks_obtained >= self.exam_schedule.passing_marks


class Timetable(models.Model):
    """Class timetable model."""

    DAYS_OF_WEEK = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    assigned_class = models.ForeignKey(
        "students.Class", on_delete=models.CASCADE, related_name="timetables"
    )
    subject = models.ForeignKey(
        "students.Subject", on_delete=models.CASCADE, related_name="timetables"
    )
    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        related_name="timetables",
    )
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200, blank=True)
    academic_year = models.ForeignKey(
        "students.AcademicYear", on_delete=models.CASCADE, related_name="timetables"
    )

    class Meta:
        verbose_name = "Timetable"
        verbose_name_plural = "Timetables"
        ordering = ["day", "start_time"]

    def __str__(self):
        return f"{self.assigned_class} - {self.subject} - Day {self.day}"
