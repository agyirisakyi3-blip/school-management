from django.db import models


class AdmissionQuery(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        VISIT_SCHEDULED = "visit_scheduled", "Visit Scheduled"
        ADMITTED = "admitted", "Admitted"
        REJECTED = "rejected", "Rejected"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    student_name = models.CharField(max_length=100, blank=True)
    class_interested = models.ForeignKey(
        "students.Class",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admission_queries",
    )
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Admission Query"
        verbose_name_plural = "Admission Queries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.status}"


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    purpose = models.CharField(max_length=200)
    person_to_meet = models.CharField(max_length=100, blank=True)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"
        ordering = ["-check_in"]

    def __str__(self):
        return f"{self.name} - {self.purpose}"


class Complaint(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    complaint_type = models.CharField(
        max_length=50,
        choices=[
            ("academic", "Academic"),
            ("administrative", "Administrative"),
            ("facility", "Facility"),
            ("harassment", "Harassment"),
            ("other", "Other"),
        ],
    )
    complainant_name = models.CharField(max_length=100)
    complainant_email = models.EmailField()
    complainant_phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    assigned_to = models.CharField(max_length=100, blank=True)
    resolution = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"
