from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import LeaveType, LeaveRequest
from .forms import LeaveTypeForm, LeaveRequestForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class LeaveDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        leave_types = LeaveType.objects.all().order_by("-created_at")
        leave_requests = (
            LeaveRequest.objects.select_related("user", "leave_type", "approved_by")
            .all()
            .order_by("-created_at")
        )
        context = {
            "leave_types": leave_types,
            "leave_requests": leave_requests,
        }
        return render(request, "leaves/leave_list.html", context)


class LeaveTypeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = "leaves/leave_type_form.html"
    success_url = reverse_lazy("leaves:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Leave type added successfully.")
        return super().form_valid(form)


class LeaveTypeUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = "leaves/leave_type_form.html"
    success_url = reverse_lazy("leaves:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Leave type updated successfully.")
        return super().form_valid(form)


class LeaveTypeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = LeaveType
    template_name = "leaves/confirm_delete.html"
    success_url = reverse_lazy("leaves:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Leave type deleted successfully.")
        return super().delete(request, *args, **kwargs)


class LeaveRequestCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = "leaves/leave_request_form.html"
    success_url = reverse_lazy("leaves:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Leave request submitted successfully.")
        return super().form_valid(form)


class LeaveRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = "leaves/leave_request_form.html"
    success_url = reverse_lazy("leaves:dashboard")

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Leave request updated successfully.")
        return super().form_valid(form)


class ApproveLeaveView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        leave_request = LeaveRequest.objects.get(pk=pk)
        leave_request.status = "approved"
        leave_request.approved_by = request.user
        leave_request.approved_at = timezone.now()
        leave_request.save()
        messages.success(request, "Leave request approved.")
        return redirect("leaves:dashboard")


class RejectLeaveView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        leave_request = LeaveRequest.objects.get(pk=pk)
        leave_request.status = "rejected"
        leave_request.approved_by = request.user
        leave_request.approved_at = timezone.now()
        leave_request.remarks = request.POST.get("remarks", "")
        leave_request.save()
        messages.success(request, "Leave request rejected.")
        return redirect("leaves:dashboard")


class CancelLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        leave_request = LeaveRequest.objects.get(pk=pk, user=request.user)
        if leave_request.status == "pending":
            leave_request.status = "cancelled"
            leave_request.save()
            messages.success(request, "Leave request cancelled.")
        else:
            messages.error(request, "Cannot cancel this leave request.")
        return redirect("leaves:dashboard")
