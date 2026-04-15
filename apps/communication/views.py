from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from .models import Announcement, Message, Notification, Contact
from .forms import AnnouncementForm, MessageForm, MessageReplyForm, ContactForm
from .utils import send_announcement_email, send_email, send_notification_email
from ..students.models import Student


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = "communication/announcement_list.html"
    context_object_name = "announcements"

    def get_queryset(self):
        queryset = Announcement.objects.filter(is_active=True)

        user_role = self.request.user.role
        queryset = queryset.filter(
            Q(target_roles__icontains=user_role) | Q(target_roles="all")
        )

        if self.request.user.is_teacher or self.request.user.is_student:
            student = Student.objects.filter(user=self.request.user).first()
            if student and student.current_class:
                queryset = queryset.filter(
                    Q(target_classes=student.current_class)
                    | Q(target_classes__isnull=True)
                )

        return queryset.distinct().order_by("-publish_date")


class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = "communication/announcement_detail.html"
    context_object_name = "announcement"


class AnnouncementCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "communication/announcement_form.html"
    success_url = reverse_lazy("communication:announcement_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        announcement = form.save()

        send_announcement_email(announcement)

        messages.success(
            self.request,
            "Announcement published successfully. Email notifications sent.",
        )
        return super().form_valid(form)


class MessageInboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "communication/message_inbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).select_related(
            "sender"
        )


class MessageSentView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "communication/message_sent.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).select_related(
            "recipient"
        )


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "communication/message_form.html"
    success_url = reverse_lazy("communication:message_inbox")

    def form_valid(self, form):
        form.instance.sender = self.request.user
        messages.success(self.request, "Message sent successfully.")
        return super().form_valid(form)


class MessageReplyView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageReplyForm
    template_name = "communication/message_reply.html"
    success_url = reverse_lazy("communication:message_inbox")

    def form_valid(self, form):
        original_message = self.get_object()
        Message.objects.create(
            sender=self.request.user,
            recipient=original_message.sender,
            subject=f"Re: {original_message.subject}",
            body=form.cleaned_data["body"],
        )
        messages.success(self.request, "Reply sent successfully.")
        return redirect(self.success_url)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "communication/message_detail.html"
    context_object_name = "message"

    def get_queryset(self):
        return Message.objects.filter(
            Q(recipient=self.request.user) | Q(sender=self.request.user)
        )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        message = self.get_object()
        if not message.is_read and message.recipient == request.user:
            message.is_read = True
            message.save()
        return response


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "communication/notification_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    def get(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(
            is_read=True
        )
        messages.success(request, "All notifications marked as read.")
        return redirect("communication:notification_list")


class MarkNotificationReadView(LoginRequiredMixin, UpdateView):
    model = Notification
    fields = ["is_read"]
    template_name = "communication/notification_detail.html"

    def get_success_url(self):
        return reverse_lazy("communication:notification_list")

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class ContactListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Contact
    template_name = "communication/contact_list.html"
    context_object_name = "contacts"


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "communication/contact_form.html"
    success_url = reverse_lazy("communication:contact_success")


class ContactReplyView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Contact
    fields = ["is_replied"]
    template_name = "communication/contact_reply.html"
    success_url = reverse_lazy("communication:contact_list")

    def form_valid(self, form):
        form.instance.replied_by = self.request.user
        messages.success(self.request, "Contact marked as replied.")
        return super().form_valid(form)
