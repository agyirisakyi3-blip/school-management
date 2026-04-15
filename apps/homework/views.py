from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
    FormView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Homework, HomeworkSubmission
from .forms import HomeworkForm, HomeworkSubmissionForm, HomeworkEvaluationForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_teacher or self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class HomeworkListView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = "homework/homework_list.html"
    context_object_name = "homeworks"

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Homework.objects.filter(teacher=user).select_related(
                "subject", "class_obj"
            )
        elif user.is_student:
            student = getattr(user, "student", None)
            if student:
                return Homework.objects.filter(
                    class_obj=student.class_obj, is_active=True
                ).select_related("subject", "class_obj", "teacher")
        return Homework.objects.select_related("subject", "class_obj", "teacher").all()


class HomeworkCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = "homework/homework_form.html"
    success_url = reverse_lazy("homework:list")

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, "Homework assigned successfully.")
        return super().form_valid(form)


class HomeworkUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = "homework/homework_form.html"
    success_url = reverse_lazy("homework:list")

    def form_valid(self, form):
        messages.success(self.request, "Homework updated successfully.")
        return super().form_valid(form)


class HomeworkDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Homework
    template_name = "homework/confirm_delete.html"
    success_url = reverse_lazy("homework:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Homework deleted successfully.")
        return super().delete(request, *args, **kwargs)


class HomeworkSubmissionView(LoginRequiredMixin, CreateView):
    model = HomeworkSubmission
    form_class = HomeworkSubmissionForm
    template_name = "homework/submit_homework.html"

    def get_success_url(self):
        return reverse_lazy("homework:list")

    def get_homework(self):
        return get_object_or_404(Homework, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        homework = self.get_homework()
        if HomeworkSubmission.objects.filter(
            homework=homework, student__user=request.user
        ).exists():
            messages.warning(request, "You have already submitted this homework.")
            return redirect("homework:list")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["homework"] = self.get_homework()
        return context

    def form_valid(self, form):
        homework = self.get_homework()
        student = self.request.user.student
        form.instance.homework = homework
        form.instance.student = student
        messages.success(self.request, "Homework submitted successfully.")
        return super().form_valid(form)


class SubmissionListView(LoginRequiredMixin, View):
    def get(self, request, homework_id):
        homework = get_object_or_404(Homework, pk=homework_id)
        if request.user.is_teacher and homework.teacher != request.user:
            if not request.user.is_admin_user:
                messages.error(
                    request, "You can only view submissions for your homework."
                )
                return redirect("homework:list")
        submissions = HomeworkSubmission.objects.filter(
            homework=homework
        ).select_related("student", "student__user")
        context = {
            "homework": homework,
            "submissions": submissions,
        }
        return render(request, "homework/submission_list.html", context)


class EvaluateSubmissionView(LoginRequiredMixin, UpdateView):
    model = HomeworkSubmission
    form_class = HomeworkEvaluationForm
    template_name = "homework/evaluate_submission.html"

    def get_success_url(self):
        homework_id = self.get_object().homework.id
        return reverse_lazy("homework:submissions", kwargs={"homework_id": homework_id})

    def form_valid(self, form):
        form.instance.evaluated_at = timezone.now()
        messages.success(self.request, "Submission evaluated successfully.")
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_teacher:
            return HomeworkSubmission.objects.filter(
                homework__teacher=self.request.user
            )
        return HomeworkSubmission.objects.all()
