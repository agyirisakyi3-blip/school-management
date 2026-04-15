from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from .models import TransportRoute, Vehicle, VehicleRoute, StudentTransport
from .forms import (
    TransportRouteForm,
    VehicleForm,
    VehicleRouteForm,
    StudentTransportForm,
)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class TransportDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "routes": TransportRoute.objects.all().order_by("-created_at"),
            "vehicles": Vehicle.objects.all().order_by("-created_at"),
            "assignments": VehicleRoute.objects.select_related("route", "vehicle")
            .all()
            .order_by("-created_at"),
            "student_transports": StudentTransport.objects.select_related(
                "student",
                "student__user",
                "vehicle_route",
                "vehicle_route__vehicle",
                "vehicle_route__route",
            )
            .all()
            .order_by("-assigned_date"),
        }
        return render(request, "transport/transport_list.html", context)


from django.shortcuts import render


# Routes
class RouteListView(LoginRequiredMixin, ListView):
    model = TransportRoute
    template_name = "transport/route_list.html"
    context_object_name = "routes"


class RouteCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TransportRoute
    form_class = TransportRouteForm
    template_name = "transport/route_form.html"
    success_url = reverse_lazy("transport:route_list")

    def form_valid(self, form):
        messages.success(self.request, "Route created successfully.")
        return super().form_valid(form)


class RouteUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = TransportRoute
    form_class = TransportRouteForm
    template_name = "transport/route_form.html"
    success_url = reverse_lazy("transport:route_list")

    def form_valid(self, form):
        messages.success(self.request, "Route updated successfully.")
        return super().form_valid(form)


class RouteDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = TransportRoute
    template_name = "transport/confirm_delete.html"
    success_url = reverse_lazy("transport:route_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Route deleted successfully.")
        return super().delete(request, *args, **kwargs)


# Vehicles
class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = "transport/vehicle_list.html"
    context_object_name = "vehicles"


class VehicleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "transport/vehicle_form.html"
    success_url = reverse_lazy("transport:vehicle_list")

    def form_valid(self, form):
        messages.success(self.request, "Vehicle added successfully.")
        return super().form_valid(form)


class VehicleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "transport/vehicle_form.html"
    success_url = reverse_lazy("transport:vehicle_list")

    def form_valid(self, form):
        messages.success(self.request, "Vehicle updated successfully.")
        return super().form_valid(form)


class VehicleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Vehicle
    template_name = "transport/confirm_delete.html"
    success_url = reverse_lazy("transport:vehicle_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Vehicle deleted successfully.")
        return super().delete(request, *args, **kwargs)


# Vehicle Routes
class VehicleRouteListView(LoginRequiredMixin, ListView):
    model = VehicleRoute
    template_name = "transport/vehicle_route_list.html"
    context_object_name = "assignments"


class VehicleRouteCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = VehicleRoute
    form_class = VehicleRouteForm
    template_name = "transport/vehicle_route_form.html"
    success_url = reverse_lazy("transport:vehicle_route_list")

    def form_valid(self, form):
        messages.success(self.request, "Route assigned successfully.")
        return super().form_valid(form)


class VehicleRouteUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = VehicleRoute
    form_class = VehicleRouteForm
    template_name = "transport/vehicle_route_form.html"
    success_url = reverse_lazy("transport:vehicle_route_list")

    def form_valid(self, form):
        messages.success(self.request, "Route assignment updated.")
        return super().form_valid(form)


class VehicleRouteDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = VehicleRoute
    template_name = "transport/confirm_delete.html"
    success_url = reverse_lazy("transport:vehicle_route_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Route assignment deleted.")
        return super().delete(request, *args, **kwargs)


# Student Transport Assignment
class StudentTransportListView(LoginRequiredMixin, ListView):
    model = StudentTransport
    template_name = "transport/student_transport_list.html"
    context_object_name = "assignments"

    def get_queryset(self):
        if self.request.user.is_student:
            return StudentTransport.objects.filter(
                student__user=self.request.user
            ).select_related(
                "vehicle_route", "vehicle_route__vehicle", "vehicle_route__route"
            )
        return StudentTransport.objects.select_related(
            "student",
            "student__user",
            "vehicle_route",
            "vehicle_route__vehicle",
            "vehicle_route__route",
        )


class StudentTransportCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = StudentTransport
    form_class = StudentTransportForm
    template_name = "transport/student_transport_form.html"
    success_url = reverse_lazy("transport:student_transport_list")

    def form_valid(self, form):
        messages.success(self.request, "Transport assigned successfully.")
        return super().form_valid(form)
