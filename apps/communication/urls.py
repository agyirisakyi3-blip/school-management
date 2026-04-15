from django.urls import path
from django.views.generic import TemplateView, RedirectView
from . import views

app_name = "communication"

urlpatterns = [
    path("", RedirectView.as_view(url="announcements/", permanent=False), name="index"),
    path(
        "announcements/", views.AnnouncementListView.as_view(), name="announcement_list"
    ),
    path(
        "announcements/create/",
        views.AnnouncementCreateView.as_view(),
        name="announcement_create",
    ),
    path(
        "announcements/<int:pk>/",
        views.AnnouncementDetailView.as_view(),
        name="announcement_detail",
    ),
    path("messages/", views.MessageInboxView.as_view(), name="message_inbox"),
    path("messages/sent/", views.MessageSentView.as_view(), name="message_sent"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"
    ),
    path(
        "messages/<int:pk>/reply/",
        views.MessageReplyView.as_view(),
        name="message_reply",
    ),
    path(
        "notifications/", views.NotificationListView.as_view(), name="notification_list"
    ),
    path(
        "notifications/mark-all-read/",
        views.MarkAllNotificationsReadView.as_view(),
        name="notification_mark_all_read",
    ),
    path(
        "notifications/<int:pk>/",
        views.MarkNotificationReadView.as_view(),
        name="notification_read",
    ),
    path(
        "notifications/<int:pk>/detail/",
        views.MarkNotificationReadView.as_view(),
        name="notification_detail",
    ),
    path("contacts/", views.ContactListView.as_view(), name="contact_list"),
    path("contacts/create/", views.ContactCreateView.as_view(), name="contact_create"),
    path(
        "contacts/<int:pk>/reply/",
        views.ContactReplyView.as_view(),
        name="contact_reply",
    ),
    path(
        "contact-success/",
        TemplateView.as_view(template_name="communication/contact_success.html"),
        name="contact_success",
    ),
]
