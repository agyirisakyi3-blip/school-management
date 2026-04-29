from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
    TemplateView,
    FormView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Student, Class, Subject, AcademicYear, AdmissionApplication
from .forms import (
    StudentCreationForm,
    StudentForm,
    ClassForm,
    SubjectForm,
    AcademicYearForm,
)
from ..finance.models import StudentFee


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return super().handle_no_permission()


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    paginate_by = 20

    def get_queryset(self):
        queryset = Student.objects.select_related("user", "current_class")

        search = self.request.GET.get("search")
        class_filter = self.request.GET.get("class")
        status = self.request.GET.get("status")

        if search:
            queryset = queryset.filter(
                Q(student_id__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(guardian_name__icontains=search)
            )

        if class_filter:
            queryset = queryset.filter(current_class_id=class_filter)

        if status == "active":
            queryset = queryset.filter(is_active=True)
        elif status == "inactive":
            queryset = queryset.filter(is_active=False)

        sort = self.request.GET.get("sort", "-created_at")
        if sort == "name":
            queryset = queryset.order_by("user__first_name")
        elif sort == "name_desc":
            queryset = queryset.order_by("-user__first_name")
        elif sort == "roll":
            queryset = queryset.order_by("roll_number")
        else:
            queryset = queryset.order_by("-created_at")

        if self.request.user.is_student:
            return queryset.filter(user=self.request.user)
        if self.request.user.is_teacher:
            teacher_class = Class.objects.filter(
                class_teacher=self.request.user
            ).first()
            if teacher_class:
                return queryset.filter(current_class=teacher_class)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classes"] = Class.objects.all()
        context["search"] = self.request.GET.get("search", "")
        context["class_filter"] = self.request.GET.get("class", "")
        context["status_filter"] = self.request.GET.get("status", "")
        context["sort_by"] = self.request.GET.get("sort", "-created_at")
        context["total_students"] = Student.objects.count()
        context["active_students"] = Student.objects.filter(is_active=True).count()
        context["classes_count"] = Class.objects.count()
        return context


class StudentBulkActionView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Handle bulk actions on students."""

    def post(self, request):
        action = request.POST.get("action")
        student_ids = request.POST.getlist("student_ids")

        if not student_ids:
            messages.error(request, "No students selected.")
            return redirect("students:student_list")

        students = Student.objects.filter(pk__in=student_ids)

        if action == "activate":
            students.update(is_active=True)
            messages.success(request, f"{students.count()} students activated.")
        elif action == "deactivate":
            students.update(is_active=False)
            messages.success(request, f"{students.count()} students deactivated.")
        elif action == "delete":
            count = students.count()
            students.delete()
            messages.success(request, f"{count} students deleted.")
        elif action == "export":
            return self.export_students(students)
        else:
            messages.error(request, "Invalid action.")

        return redirect("students:student_list")

    def export_students(self, students):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=students.csv"
        response.write("ID,Name,Email,Class,Roll No,Guardian,Phone,Status\n")
        for s in students:
            response.write(
                f"{s.student_id},{s.user.get_full_name()},{s.user.email},"
                f"{s.current_class},{s.roll_number},{s.guardian_name},"
                f"{s.guardian_phone},{s.is_active}\n"
            )
        return response


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"
    context_object_name = "student"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        
        # Pull models for recent record lists
        from ..academics.models import Attendance, Result
        
        # Summary details are now handled by model properties:
        # student.attendance_percentage, student.average_score, etc.
        
        context["recent_attendance"] = Attendance.objects.filter(student=student).order_by("-date")[:5]
        context["recent_results"] = Result.objects.filter(student=student).select_related(
            "exam_schedule__subject", "exam_schedule__exam"
        ).order_by("-created_at")[:5]
        
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Student.objects.select_related("user", "current_class")
        
        if user.is_admin_user:
            return queryset
        if user.is_student:
            return queryset.filter(user=user)
        if user.is_teacher:
            # Teachers can see students in the classes they teach
            teacher_classes = Class.objects.filter(class_teacher=user)
            return queryset.filter(current_class__in=teacher_classes)
        if user.is_parent:
            # Parents can see their wards
            return queryset.filter(parent=user)
        
        return queryset.none()


class StudentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreationForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Admission"
        context["classes"] = Class.objects.all()
        context["academic_years"] = AcademicYear.objects.all()
        return context

    def form_valid(self, form):
        student = form.save()
        messages.success(
            self.request,
            f"Student '{student.user.get_full_name()}' created successfully with ID: {student.student_id}",
        )
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Student"
        context["classes"] = Class.objects.all()
        context["academic_years"] = AcademicYear.objects.all()
        return context

    def form_valid(self, form):
        student = form.save()
        messages.success(
            self.request,
            f"Student '{student.user.get_full_name()}' updated successfully.",
        )
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Student
    template_name = "students/student_confirm_delete.html"
    success_url = reverse_lazy("students:student_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Student deleted successfully.")
        return super().delete(request, *args, **kwargs)


class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = "students/class_list.html"
    context_object_name = "classes"
    paginate_by = 15

    def get_queryset(self):
        queryset = Class.objects.select_related(
            "academic_year", "class_teacher"
        ).prefetch_related("students", "subjects")

        search = self.request.GET.get("search")
        academic_year = self.request.GET.get("academic_year")
        sort = self.request.GET.get("sort", "-created_at")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )

        if academic_year:
            queryset = queryset.filter(academic_year_id=academic_year)

        if sort == "name":
            queryset = queryset.order_by("name")
        elif sort == "name_desc":
            queryset = queryset.order_by("-name")
        elif sort == "students_count":
            queryset = queryset.order_by("-students__count")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        context["academic_year_filter"] = self.request.GET.get("academic_year", "")
        context["sort_by"] = self.request.GET.get("sort", "-created_at")
        context["academic_years"] = AcademicYear.objects.all()

        from .models import Student, Subject

        context["total_classes"] = Class.objects.count()
        context["total_students_in_classes"] = Student.objects.filter(
            current_class__isnull=False
        ).count()
        context["classes_with_teachers"] = Class.objects.filter(
            class_teacher__isnull=False
        ).count()
        context["total_subjects"] = Subject.objects.count()
        return context


class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class
    template_name = "students/class_detail.html"
    context_object_name = "class_obj"

    def get_queryset(self):
        user = self.request.user
        queryset = Class.objects.all()
        
        if user.is_admin_user:
            return queryset
        if user.is_teacher:
            # Teachers can see the classes they are assigned to
            return queryset.filter(class_teacher=user)
        if user.is_student:
            # Students can see their own class
            return queryset.filter(students__user=user)
        if user.is_parent:
            # Parents can see their wards' classes
            return queryset.filter(students__parent=user)
            
        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = self.object.students.all()
        context["subjects"] = self.object.subjects.all()
        return context


class ClassCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = "students/class_form.html"
    success_url = reverse_lazy("students:class_list")

    def form_valid(self, form):
        messages.success(self.request, "Class created successfully.")
        return super().form_valid(form)


class ClassUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "students/class_form.html"
    success_url = reverse_lazy("students:class_list")

    def form_valid(self, form):
        messages.success(self.request, "Class updated successfully.")
        return super().form_valid(form)


class ClassDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Class
    template_name = "students/class_confirm_delete.html"
    success_url = reverse_lazy("students:class_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Class deleted successfully.")
        return super().delete(request, *args, **kwargs)


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "students/subject_list.html"
    context_object_name = "subjects"


class SubjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "students/subject_form.html"
    success_url = reverse_lazy("students:subject_list")

    def form_valid(self, form):
        messages.success(self.request, "Subject created successfully.")
        return super().form_valid(form)


class SubjectUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "students/subject_form.html"
    success_url = reverse_lazy("students:subject_list")

    def form_valid(self, form):
        messages.success(self.request, "Subject updated successfully.")
        return super().form_valid(form)


class AcademicYearListView(LoginRequiredMixin, ListView):
    model = AcademicYear
    template_name = "students/academic_year_list.html"
    context_object_name = "academic_years"


class AcademicYearCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = "students/academic_year_form.html"
    success_url = reverse_lazy("students:academic_year_list")

    def form_valid(self, form):
        if form.cleaned_data["is_current"]:
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        messages.success(self.request, "Academic year created successfully.")
        return super().form_valid(form)


# Online Admission Views
class AdmissionFormView(TemplateView):
    """Public admission form - no login required"""
    template_name = "students/admission_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classes"] = Class.objects.all()
        context["academic_years"] = AcademicYear.objects.filter(is_current=True)
        return context


class AdmissionSubmitView(View):
    """Handle admission form submission"""
    def post(self, request):
        application = AdmissionApplication.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            date_of_birth=request.POST.get("date_of_birth"),
            gender=request.POST.get("gender"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            guardian_name=request.POST.get("guardian_name"),
            guardian_phone=request.POST.get("guardian_phone"),
            guardian_email=request.POST.get("guardian_email", ""),
            guardian_relation=request.POST.get("guardian_relation"),
            guardian_occupation=request.POST.get("guardian_occupation", ""),
            current_school=request.POST.get("current_school", ""),
            current_class=request.POST.get("current_class", ""),
            grade_level=request.POST.get("grade_level"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            postal_code=request.POST.get("postal_code", ""),
            academic_year_id=request.POST.get("academic_year"),
            applied_for_class_id=request.POST.get("applied_for_class") or None,
        )
        messages.success(
            request,
            f"Thank you {application.full_name}! Your application has been submitted. "
            f"We will contact you at {application.phone} soon."
        )
        return redirect("students:admission_form")


class AdmissionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Admin list of admission applications"""
    model = AdmissionApplication
    template_name = "students/admission_list.html"
    context_object_name = "applications"
    paginate_by = 20

    def get_queryset(self):
        qs = AdmissionApplication.objects.all()
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs


class AdmissionDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    """View admission application details"""
    model = AdmissionApplication
    template_name = "students/admission_detail.html"
    context_object_name = "application"


from datetime import date

class AdmissionApproveView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Approve admission and create student"""
    def post(self, request, pk):
        app = get_object_or_404(AdmissionApplication, pk=pk)
        # Create user account
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            username=f"{app.first_name.lower()}{app.last_name.lower()}{app.pk}",
            email=app.email,
            password="Welcome@123",
            first_name=app.first_name,
            last_name=app.last_name,
            role=User.Role.STUDENT,
        )
        # Create student record
        student = Student.objects.create(
            user=user,
            student_id=f"ST{str(AdmissionApplication.objects.count()+1).zfill(5)}",
            admission_date=date.today(),
            current_class=app.applied_for_class,
            guardian_name=app.guardian_name,
            guardian_phone=app.guardian_phone,
            guardian_relation=app.guardian_relation,
        )
        # Update application
        app.status = "approved"
        app.assigned_student = student
        app.notes = f"Approved. Student ID: {student.student_id}"
        app.save()
        messages.success(request, f"Student created! ID: {student.student_id}")
        return redirect("students:admission_list")
