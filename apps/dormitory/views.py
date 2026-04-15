from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Dormitory, Room, StudentRoom
from .forms import DormitoryForm, RoomForm, StudentRoomForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class DormitoryDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "dormitories": Dormitory.objects.all().order_by("-created_at"),
            "rooms": Room.objects.select_related("dormitory")
            .all()
            .order_by("-created_at"),
            "assignments": StudentRoom.objects.select_related(
                "student", "student__user", "room", "room__dormitory"
            )
            .all()
            .order_by("-created_at"),
        }
        return render(request, "dormitory/dormitory_list.html", context)


class DormitoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Dormitory
    form_class = DormitoryForm
    template_name = "dormitory/dormitory_form.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Dormitory added successfully.")
        return super().form_valid(form)


class DormitoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Dormitory
    form_class = DormitoryForm
    template_name = "dormitory/dormitory_form.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Dormitory updated successfully.")
        return super().form_valid(form)


class DormitoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Dormitory
    template_name = "dormitory/confirm_delete.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Dormitory deleted successfully.")
        return super().delete(request, *args, **kwargs)


class RoomCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "dormitory/room_form.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Room added successfully.")
        return super().form_valid(form)


class RoomUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "dormitory/room_form.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Room updated successfully.")
        return super().form_valid(form)


class RoomDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Room
    template_name = "dormitory/confirm_delete.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Room deleted successfully.")
        return super().delete(request, *args, **kwargs)


class StudentRoomCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = StudentRoom
    form_class = StudentRoomForm
    template_name = "dormitory/student_room_form.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Student assigned to room successfully.")
        return super().form_valid(form)


class StudentRoomDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = StudentRoom
    template_name = "dormitory/confirm_delete.html"
    success_url = reverse_lazy("dormitory:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Room assignment removed.")
        return super().delete(request, *args, **kwargs)
