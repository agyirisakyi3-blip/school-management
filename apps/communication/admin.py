from django.contrib import admin
from .models import Announcement, Message, Notification, Contact


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "priority", "created_by", "is_active", "publish_date"]
    list_filter = ["priority", "is_active", "publish_date"]
    search_fields = ["title", "content"]
    filter_horizontal = ["target_classes"]
    readonly_fields = ["created_at"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "recipient", "subject", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["sender__username", "recipient__username", "subject"]
    readonly_fields = ["created_at"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["recipient", "notification_type", "title", "is_read", "created_at"]
    list_filter = ["notification_type", "is_read", "created_at"]
    search_fields = ["recipient__username", "title", "message"]
    readonly_fields = ["created_at"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_replied", "created_at"]
    list_filter = ["is_replied", "created_at"]
    search_fields = ["name", "email", "subject"]
    readonly_fields = ["created_at"]
