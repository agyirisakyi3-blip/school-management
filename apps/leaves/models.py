from django.db import models
from django.conf import settings


class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    days_allowed = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    requires_approval = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Leave Type"
        verbose_name_plural = "Leave Types"

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_leaves",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.get_full_name} - {self.leave_type.name} ({self.start_date} to {self.end_date})"

    def get_total_days(self):
        return (self.end_date - self.start_date).days + 1
