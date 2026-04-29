from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with role-based access control."""

    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        TEACHER = "teacher", _("Teacher")
        STUDENT = "student", _("Student")
        PARENT = "parent", _("Parent")
        # Non-teaching staff
        ACCOUNTANT = "accountant", _("Accountant")
        LIBRARIAN = "librarian", _("Librarian")
        RECEPTIONIST = "receptionist", _("Receptionist")
        DRIVER = "driver", _("Driver")
        COOK = "cook", _("Cook")
        GUARD = "guard", _("Security Guard")
        CLEANER = "cleaner", _("Cleaner")
        MAINTENANCE = "maintenance", _("Maintenance")
        COUNSELOR = "counselor", _("Counselor")
        NURSE = "nurse", _("School Nurse")

    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        OTHER = "other", _("Other")

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT

    @property
    def is_staff_member(self):
        """Check if user is non-teaching staff."""
        return self.role in [
            self.Role.ACCOUNTANT,
            self.Role.LIBRARIAN,
            self.Role.RECEPTIONIST,
            self.Role.DRIVER,
            self.Role.COOK,
            self.Role.GUARD,
            self.Role.CLEANER,
            self.Role.MAINTENANCE,
            self.Role.COUNSELOR,
            self.Role.NURSE,
        ]

    @property
    def is_teaching_staff(self):
        """Check if user is teacher."""
        return self.role == self.Role.TEACHER

    @property
    def get_staff_type_display_name(self):
        """Get display name for non-teaching staff."""
        non_teaching_roles = {
            "accountant": "Accountant",
            "librarian": "Librarian",
            "receptionist": "Receptionist",
            "driver": "Driver",
            "cook": "Cook",
            "guard": "Security Guard",
            "cleaner": "Cleaner",
            "maintenance": "Maintenance Staff",
            "counselor": "Counselor",
            "nurse": "School Nurse",
        }
        return non_teaching_roles.get(self.role, self.get_role_display())


class UserProfile(models.Model):
    """Extended profile information for users."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"


class ActivityLog(models.Model):
    """Tracks all administrative actions for audit trail."""

    class ActionType(models.TextChoices):
        CREATE = "create", _("Created")
        UPDATE = "update", _("Updated")
        DELETE = "delete", _("Deleted")
        LOGIN = "login", _("Logged In")
        LOGOUT = "logout", _("Logged Out")
        EXPORT = "export", _("Exported")
        IMPORT = "import", _("Imported")
        OTHER = "other", _("Other")

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="activity_logs"
    )
    action = models.CharField(max_length=20, choices=ActionType.choices)
    category = models.CharField(max_length=50, default="system")
    description = models.TextField()
    target_model = models.CharField(max_length=100, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Activity Log")
        verbose_name_plural = _("Activity Logs")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.description[:50]}"

    @classmethod
    def log(
        cls,
        user,
        action,
        description,
        category="system",
        target_model="",
        target_id=None,
        ip_address=None,
    ):
        """Convenience method to create a log entry."""
        return cls.objects.create(
            user=user,
            action=action,
            description=description,
            category=category,
            target_model=target_model,
            target_id=target_id,
            ip_address=ip_address,
        )


class NonTeachingStaff(models.Model):
    """Non-teaching staff profile model."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile"
    )
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    employment_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contract_type = models.CharField(
        max_length=20,
        choices=[
            ("permanent", "Permanent"),
            ("contract", "Contract"),
            ("part_time", "Part-time"),
            ("temporary", "Temporary"),
        ],
        default="permanent",
    )
    shift_timing = models.CharField(max_length=50, blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    qualifications = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.get_role_display()})"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            last_staff = NonTeachingStaff.objects.order_by("-id").first()
            if last_staff and last_staff.staff_id:
                try:
                    num = int(last_staff.staff_id.replace("STAFF", ""))
                    self.staff_id = f"STAFF{str(num + 1).zfill(5)}"
                except (ValueError, TypeError):
                    self.staff_id = "STAFF00001"
            else:
                self.staff_id = "STAFF00001"
        super().save(*args, **kwargs)
