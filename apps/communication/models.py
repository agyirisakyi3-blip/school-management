from django.db import models
from django.conf import settings


class Announcement(models.Model):
    """Announcement model."""

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.MEDIUM
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_announcements",
    )
    target_roles = models.CharField(max_length=200, blank=True, default="all")
    target_classes = models.ManyToManyField(
        "students.Class", blank=True, related_name="announcements"
    )
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ["-publish_date"]

    def __str__(self):
        return self.title

    def get_target_roles_list(self):
        if self.target_roles == "all" or not self.target_roles:
            return ["admin", "teacher", "student", "parent"]
        return [role.strip() for role in self.target_roles.split(",")]


class Message(models.Model):
    """Messaging model."""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.subject}"


class Notification(models.Model):
    """Notification model."""

    class NotificationType(models.TextChoices):
        ANNOUNCEMENT = "announcement", "Announcement"
        ATTENDANCE = "attendance", "Attendance"
        RESULT = "result", "Result"
        FEE = "fee", "Fee"
        MESSAGE = "message", "Message"
        SYSTEM = "system", "System"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient}: {self.title}"


class Contact(models.Model):
    """Contact/Enquiry model."""

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_replied = models.BooleanField(default=False)
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replied_contacts",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"
