from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import AdmissionQuery, Visitor, Complaint
from .forms import AdmissionQueryForm, VisitorForm, ComplaintForm, ComplaintUpdateForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class FrontdeskDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "queries": AdmissionQuery.objects.select_related("class_interested")
            .all()
            .order_by("-created_at")[:10],
            "visitors": Visitor.objects.all().order_by("-check_in")[:10],
            "complaints": Complaint.objects.all().order_by("-created_at")[:10],
        }
        return render(request, "frontdesk/frontdesk_list.html", context)


class AdmissionQueryCreateView(LoginRequiredMixin, CreateView):
    model = AdmissionQuery
    form_class = AdmissionQueryForm
    template_name = "frontdesk/query_form.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Admission query submitted successfully.")
        return super().form_valid(form)


class AdmissionQueryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = AdmissionQuery
    form_class = AdmissionQueryForm
    template_name = "frontdesk/query_form.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Query updated successfully.")
        return super().form_valid(form)


class AdmissionQueryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = AdmissionQuery
    template_name = "frontdesk/confirm_delete.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Query deleted successfully.")
        return super().delete(request, *args, **kwargs)


class VisitorCreateView(LoginRequiredMixin, CreateView):
    model = Visitor
    form_class = VisitorForm
    template_name = "frontdesk/visitor_form.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Visitor checked in successfully.")
        return super().form_valid(form)


class VisitorCheckOutView(LoginRequiredMixin, View):
    def post(self, request, pk):
        visitor = Visitor.objects.get(pk=pk)
        visitor.check_out = timezone.now()
        visitor.save()
        messages.success(request, "Visitor checked out successfully.")
        return redirect("frontdesk:dashboard")


class VisitorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Visitor
    template_name = "frontdesk/confirm_delete.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Visitor record deleted successfully.")
        return super().delete(request, *args, **kwargs)


class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = "frontdesk/complaint_form.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Complaint submitted successfully.")
        return super().form_valid(form)


class ComplaintUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Complaint
    form_class = ComplaintUpdateForm
    template_name = "frontdesk/complaint_update_form.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Complaint updated successfully.")
        return super().form_valid(form)


class ComplaintDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Complaint
    template_name = "frontdesk/confirm_delete.html"
    success_url = reverse_lazy("frontdesk:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Complaint deleted successfully.")
        return super().delete(request, *args, **kwargs)
