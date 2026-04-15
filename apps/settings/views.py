from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    SchoolInfo,
    GeneralSettings,
    EmailSettings,
    ThemeSettings,
    AttendanceSettings,
    ResultSettings,
    FeeSettings,
)
from .forms import (
    SchoolInfoForm,
    GeneralSettingsForm,
    EmailSettingsForm,
    ThemeSettingsForm,
    AttendanceSettingsForm,
    ResultSettingsForm,
    FeeSettingsForm,
)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class SettingsDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "settings/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["school_info"] = SchoolInfo.get_instance()
        context["general_settings"] = GeneralSettings.get_instance()
        context["email_settings"] = EmailSettings.get_instance()
        context["theme_settings"] = ThemeSettings.get_instance()
        context["attendance_settings"] = AttendanceSettings.get_instance()
        context["result_settings"] = ResultSettings.get_instance()
        context["fee_settings"] = FeeSettings.get_instance()
        return context


class SchoolInfoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = SchoolInfo
    form_class = SchoolInfoForm
    template_name = "settings/school_info.html"

    def get_object(self):
        return SchoolInfo.get_instance()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "School information updated successfully!")
        return redirect("settings:school_info")


class GeneralSettingsUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = GeneralSettings
    form_class = GeneralSettingsForm
    template_name = "settings/general_settings.html"

    def get_object(self):
        return GeneralSettings.get_instance()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "General settings updated successfully!")
        return redirect("settings:general_settings")


class EmailSettingsUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = EmailSettings
    form_class = EmailSettingsForm
    template_name = "settings/email_settings.html"

    def get_object(self):
        return EmailSettings.get_instance()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Email settings updated successfully!")
        return redirect("settings:email_settings")

    def post(self, request, *args, **kwargs):
        if "test_email" in request.POST:
            return self.send_test_email(request)
        return super().post(request, *args, **kwargs)

    def send_test_email(self, request):
        email_settings = EmailSettings.get_instance()
        test_email = (
            request.POST.get("test_email_recipient")
            or email_settings.test_email_recipient
        )

        if not test_email:
            messages.error(request, "Please enter a test email address.")
            return redirect("settings:email_settings")

        try:
            send_mail(
                subject="Test Email - School Management System",
                message="This is a test email from your School Management System. If you received this, your email settings are configured correctly.",
                from_email=email_settings.email_from_address
                or settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False,
            )
            messages.success(request, f"Test email sent to {test_email}")
        except Exception as e:
            messages.error(request, f"Failed to send test email: {str(e)}")

        return redirect("settings:email_settings")


class ThemeSettingsUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ThemeSettings
    form_class = ThemeSettingsForm
    template_name = "settings/theme_settings.html"

    def get_object(self):
        return ThemeSettings.get_instance()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Theme settings updated successfully!")
        return redirect("settings:theme_settings")


class AttendanceSettingsUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = AttendanceSettings
    form_class = AttendanceSettingsForm
    template_name = "settings/attendance_settings.html"

    def get_object(self):
        return AttendanceSettings.get_instance()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Attendance settings updated successfully!")
        return redirect("settings:attendance_settings")


class ResultSettingsUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ResultSettings
    form_class = ResultSettingsForm
    template_name = "settings/result_settings.html"

    def get_object(self):
        return ResultSettings.get_instance()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Result settings updated successfully!")
        return redirect("settings:result_settings")


class FeeSettingsUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FeeSettings
    form_class = FeeSettingsForm
    template_name = "settings/fee_settings.html"

    def get_object(self):
        return FeeSettings.get_instance()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Fee settings updated successfully!")
        return redirect("settings:fee_settings")
