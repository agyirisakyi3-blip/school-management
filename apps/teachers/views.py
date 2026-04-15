from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from .models import Teacher, TeacherSubject
from .forms import TeacherCreationForm, TeacherForm, TeacherSubjectForm
from .models import Teacher, TeacherSubject


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return super().handle_no_permission()


class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = "teachers/teacher_list.html"
    context_object_name = "teachers"
    paginate_by = 20

    def get_queryset(self):
        queryset = Teacher.objects.select_related("user").annotate(
            subjects_count=Count("teacher_subjects"),
            classes_count=Count("teacher_subjects__assigned_class", distinct=True),
        )

        search = self.request.GET.get("search")
        department = self.request.GET.get("department")
        status = self.request.GET.get("status")

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(employee_id__icontains=search)
                | Q(qualification__icontains=search)
            )

        if department:
            queryset = queryset.filter(department__icontains=department)

        if status == "active":
            queryset = queryset.filter(is_active=True)
        elif status == "inactive":
            queryset = queryset.filter(is_active=False)

        sort_by = self.request.GET.get("sort", "-created_at")
        if sort_by == "name":
            queryset = queryset.order_by("user__first_name")
        elif sort_by == "name_desc":
            queryset = queryset.order_by("-user__first_name")
        elif sort_by == "employee_id":
            queryset = queryset.order_by("employee_id")
        else:
            queryset = queryset.order_by("-created_at")

        if self.request.user.is_teacher:
            return queryset.filter(user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_teachers"] = Teacher.objects.count()
        context["active_teachers"] = Teacher.objects.filter(is_active=True).count()
        context["departments"] = (
            Teacher.objects.exclude(department="")
            .values_list("department", flat=True)
            .distinct()
        )
        context["search"] = self.request.GET.get("search", "")
        context["department_filter"] = self.request.GET.get("department", "")
        context["status_filter"] = self.request.GET.get("status", "")
        context["sort_by"] = self.request.GET.get("sort", "-created_at")
        return context


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = "teachers/teacher_detail.html"
    context_object_name = "teacher"

    def get_queryset(self):
        return Teacher.objects.select_related("user")


class TeacherCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherCreationForm
    template_name = "teachers/teacher_form.html"
    success_url = reverse_lazy("teachers:teacher_list")

    def form_valid(self, form):
        messages.success(self.request, "Teacher created successfully.")
        return super().form_valid(form)


class TeacherUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "teachers/teacher_form.html"
    success_url = reverse_lazy("teachers:teacher_list")

    def form_valid(self, form):
        messages.success(self.request, "Teacher updated successfully.")
        return super().form_valid(form)


class TeacherDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Teacher
    template_name = "teachers/teacher_confirm_delete.html"
    success_url = reverse_lazy("teachers:teacher_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Teacher deleted successfully.")
        return super().delete(request, *args, **kwargs)


class TeacherSubjectListView(LoginRequiredMixin, ListView):
    model = TeacherSubject
    template_name = "teachers/teacher_subject_list.html"
    context_object_name = "assignments"

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            teacher_profile = Teacher.objects.filter(user=user).first()
            if teacher_profile:
                return TeacherSubject.objects.filter(teacher=teacher_profile)
            return TeacherSubject.objects.none()
        return TeacherSubject.objects.select_related(
            "teacher", "subject", "assigned_class"
        )


class TeacherSubjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = TeacherSubject
    form_class = TeacherSubjectForm
    template_name = "teachers/teacher_subject_form.html"
    success_url = reverse_lazy("teachers:teacher_subject_list")

    def form_valid(self, form):
        messages.success(self.request, "Subject assigned successfully.")
        return super().form_valid(form)
