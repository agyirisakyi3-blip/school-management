from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""

    list_display = ["username", "email", "role", "first_name", "last_name", "is_active"]
    list_filter = ["role", "is_active", "is_staff", "created_at"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["-created_at"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "role",
                    "phone",
                    "address",
                    "profile_picture",
                    "date_of_birth",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "classes": ("wide",),
                "fields": ("email", "role", "phone"),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""

    list_display = ["user", "blood_group", "religion", "nationality"]
    search_fields = ["user__username", "user__email", "user__first_name"]
    list_filter = ["blood_group", "religion", "nationality"]
