from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from datetime import datetime, timedelta
from ..students.models import Student, Class, AcademicYear, Subject
from ..teachers.models import Teacher
from ..academics.models import Attendance, Exam, Result
from ..finance.models import (
    StudentFee,
    Payment,
    Expense,
    FeeCategory,
    FeeParticular,
    FeeGroup,
    DiscountCategory,
)
from ..communication.models import Announcement, Notification
from .models import User, ActivityLog, NonTeachingStaff
from .forms import NonTeachingStaffCreationForm, NonTeachingStaffForm


class HomeView(TemplateView):
    """Home page view."""

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:dashboard")
        return redirect("users:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    """Base dashboard view."""

    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_admin_user:
            context["total_students"] = Student.objects.filter(is_active=True).count()
            context["total_teachers"] = Teacher.objects.filter(is_active=True).count()
            context["total_classes"] = Class.objects.count()
            context["total_subjects"] = Subject.objects.count()
            context["total_fees_collected"] = (
                StudentFee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
            )
            context["pending_fees"] = StudentFee.objects.filter(
                status__in=["pending", "partial", "overdue"]
            ).count()
            context["total_fee_categories"] = FeeCategory.objects.count()
            context["total_fee_particulars"] = FeeParticular.objects.filter(
                is_active=True
            ).count()
            context["total_fee_groups"] = FeeGroup.objects.count()
            context["total_discounts"] = DiscountCategory.objects.filter(
                is_active=True
            ).count()
            context["total_exams"] = Exam.objects.filter(is_active=True).count()
            today = datetime.now().date()
            context["upcoming_exams"] = Exam.objects.filter(
                start_date__gte=today, is_active=True
            ).count()
            context["today_attendance"] = Attendance.objects.filter(date=today).count()
            context["total_results"] = Result.objects.count()
            context["recent_announcements"] = Announcement.objects.filter(
                is_active=True
            ).order_by("-created_at")[:5]
            context["recent_attendance"] = Attendance.objects.select_related(
                "student__user"
            ).order_by("-date")[:5]
            context["recent_students"] = Student.objects.select_related(
                "user", "current_class"
            ).order_by("-created_at")[:5]
            context["recent_payments"] = Payment.objects.select_related(
                "student_fee__student__user"
            ).order_by("-payment_date")[:10]

        elif user.is_teacher:
            teacher = Teacher.objects.filter(user=user).first()
            if teacher:
                context["my_students_count"] = Student.objects.filter(
                    current_class__class_teacher=user, is_active=True
                ).count()
                context["my_classes"] = Class.objects.filter(class_teacher=user)
                context["my_subjects"] = teacher.subjects.values_list(
                    "subject__name", flat=True
                )
            today = datetime.now().date()
            context["today_attendance"] = Attendance.objects.filter(
                date=today, student__current_class__class_teacher=user
            ).count()
            context["pending_results"] = Result.objects.filter(
                exam_schedule__teacher=user
            ).count()
            context["recent_announcements"] = Announcement.objects.filter(
                is_active=True
            ).order_by("-created_at")[:5]

        elif user.is_student:
            student = Student.objects.filter(user=user).first()
            if student:
                total_attendance = Attendance.objects.filter(student=student).count()
                present_attendance = Attendance.objects.filter(
                    student=student, status="present"
                ).count()
                context["attendance_percentage"] = (
                    round((present_attendance / total_attendance) * 100, 1)
                    if total_attendance > 0
                    else 0
                )
                context["student_results"] = Result.objects.filter(
                    student=student
                ).select_related("exam_schedule__subject")
                if context["student_results"]:
                    context["average_score"] = round(
                        context["student_results"].aggregate(avg=Avg("marks_obtained"))[
                            "avg"
                        ],
                        1,
                    )
                context["upcoming_exams"] = Exam.objects.filter(
                    start_date__gte=datetime.now().date()
                ).count()
                context["student_fees"] = StudentFee.objects.filter(student=student)
            context["recent_announcements"] = Announcement.objects.filter(
                is_active=True
            ).order_by("-created_at")[:5]

        elif user.is_parent:
            context["ward_students"] = Student.objects.filter(parent=user)
            for student in context["ward_students"]:
                student.total_attendance = Attendance.objects.filter(
                    student=student
                ).count()
                student.present_attendance = Attendance.objects.filter(
                    student=student, status="present"
                ).count()
            context["recent_announcements"] = Announcement.objects.filter(
                is_active=True
            ).order_by("-created_at")[:5]

        context["notifications"] = Notification.objects.filter(
            recipient=user, is_read=False
        ).count()
        return context


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard for admin users."""

    template_name = "users/dashboard_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Admin Dashboard"

        # Student & Staff Stats
        context["total_students"] = Student.objects.filter(is_active=True).count()
        context["total_teachers"] = Teacher.objects.filter(is_active=True).count()
        context["total_classes"] = Class.objects.count()
        context["total_subjects"] = Subject.objects.count()
        context["total_academic_years"] = AcademicYear.objects.count()

        # Finance Stats
        context["total_fees_collected"] = (
            StudentFee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        )
        context["total_fees_pending"] = (
            StudentFee.objects.filter(
                status__in=["pending", "partial", "overdue"]
            ).aggregate(total=Sum("amount") - Sum("amount_paid"))["total"]
            or 0
        )
        context["monthly_collections"] = (
            Payment.objects.filter(payment_date__month=datetime.now().month).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        context["monthly_expenses"] = (
            Expense.objects.filter(expense_date__month=datetime.now().month).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        context["pending_fees_count"] = StudentFee.objects.filter(
            status__in=["pending", "partial", "overdue"]
        ).count()

        # Fee Management Stats
        context["total_fee_categories"] = FeeCategory.objects.count()
        context["total_fee_particulars"] = FeeParticular.objects.filter(
            is_active=True
        ).count()
        context["total_fee_groups"] = FeeGroup.objects.count()
        context["total_discounts"] = DiscountCategory.objects.filter(
            is_active=True
        ).count()

        # Academic Stats
        context["total_exams"] = Exam.objects.filter(is_active=True).count()
        today = datetime.now().date()
        context["upcoming_exams"] = Exam.objects.filter(
            start_date__gte=today, is_active=True
        ).count()
        context["today_attendance"] = Attendance.objects.filter(date=today).count()
        context["total_results"] = Result.objects.count()

        # Recent Data
        context["recent_payments"] = Payment.objects.select_related(
            "student_fee__student__user"
        ).order_by("-payment_date")[:10]
        context["recent_students"] = Student.objects.select_related(
            "user", "current_class"
        ).order_by("-created_at")[:5]
        context["recent_attendance"] = Attendance.objects.select_related(
            "student__user"
        ).order_by("-date")[:5]

        return context


class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard for teacher users."""

    template_name = "users/dashboard_teacher.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Teacher Dashboard"
        teacher = Teacher.objects.filter(user=self.request.user).first()
        if teacher:
            context["my_classes"] = Class.objects.filter(
                class_teacher=self.request.user
            )
            context["my_students"] = Student.objects.filter(
                current_class__class_teacher=self.request.user, is_active=True
            ).count()
            today = datetime.now().date()
            context["today_attendance_count"] = Attendance.objects.filter(
                date=today, student__current_class__class_teacher=self.request.user
            ).count()
            context["total_students"] = Student.objects.filter(
                current_class__class_teacher=self.request.user, is_active=True
            ).count()
            context["my_results"] = Result.objects.filter(
                exam_schedule__teacher=self.request.user
            ).select_related("student__user", "exam_schedule__subject")[:10]
        return context


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard for student users."""

    template_name = "users/dashboard_student.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student Dashboard"
        student = Student.objects.filter(user=self.request.user).first()
        if student:
            context["student"] = student
            total = Attendance.objects.filter(student=student).count()
            present = Attendance.objects.filter(
                student=student, status="present"
            ).count()
            context["attendance_pct"] = (
                round((present / total) * 100, 1) if total > 0 else 0
            )
            context["my_results"] = Result.objects.filter(
                student=student
            ).select_related("exam_schedule__subject", "exam_schedule__exam")
            context["upcoming_exams"] = Exam.objects.filter(
                start_date__gte=datetime.now().date()
            )
            context["my_fees"] = StudentFee.objects.filter(student=student)
        return context


class ParentDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard for parent users."""

    template_name = "users/dashboard_parent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Parent Dashboard"
        context["ward_students"] = Student.objects.filter(parent=self.request.user)
        for student in context["ward_students"]:
            total = Attendance.objects.filter(student=student).count()
            present = Attendance.objects.filter(
                student=student, status="present"
            ).count()
            student.attendance_pct = (
                round((present / total) * 100, 1) if total > 0 else 0
            )
            student.recent_results = Result.objects.filter(
                student=student
            ).select_related("exam_schedule__subject")[:5]
        return context


class AdminRequiredMixin(LoginRequiredMixin):
    """Mixin that restricts access to admin users only."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_user:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("users:dashboard")
        return super().dispatch(request, *args, **kwargs)


class AdminControlPanelView(AdminRequiredMixin, TemplateView):
    """Main admin control panel with full system overview."""

    template_name = "users/admin_control_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import User, ActivityLog
        from ..library.models import Book
        from ..transport.models import Vehicle, TransportRoute
        from ..dormitory.models import Room
        from ..leaves.models import LeaveRequest
        from ..frontdesk.models import Visitor

        today = datetime.now().date()

        # User stats
        context["total_users"] = User.objects.count()
        context["admin_count"] = User.objects.filter(role="admin").count()
        context["teacher_count"] = User.objects.filter(role="teacher").count()
        context["student_count"] = User.objects.filter(role="student").count()
        context["parent_count"] = User.objects.filter(role="parent").count()
        context["active_users"] = User.objects.filter(is_active=True).count()
        context["inactive_users"] = User.objects.filter(is_active=False).count()

        # Student & Teacher stats
        context["total_students"] = Student.objects.filter(is_active=True).count()
        context["total_teachers"] = Teacher.objects.filter(is_active=True).count()
        context["total_classes"] = Class.objects.count()
        context["total_subjects"] = Subject.objects.count()
        context["total_academic_years"] = AcademicYear.objects.count()

        # Finance stats
        context["total_fees_collected"] = (
            StudentFee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        )
        context["pending_fees"] = StudentFee.objects.filter(
            status__in=["pending", "partial", "overdue"]
        ).count()
        context["monthly_collections"] = (
            Payment.objects.filter(payment_date__month=today.month).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        context["monthly_expenses"] = (
            Expense.objects.filter(expense_date__month=today.month).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        # Academic stats
        context["total_exams"] = Exam.objects.filter(is_active=True).count()
        context["upcoming_exams"] = Exam.objects.filter(
            start_date__gte=today, is_active=True
        ).count()
        context["today_attendance"] = Attendance.objects.filter(date=today).count()
        context["total_results"] = Result.objects.count()

        # Communication stats
        context["total_announcements"] = Announcement.objects.filter(
            is_active=True
        ).count()
        context["unread_notifications"] = Notification.objects.filter(
            is_read=False
        ).count()

        # Library stats
        try:
            context["total_books"] = Book.objects.count()
        except Exception:
            context["total_books"] = 0

        # Transport stats
        try:
            context["total_vehicles"] = Vehicle.objects.count()
            context["total_routes"] = TransportRoute.objects.count()
        except Exception:
            context["total_vehicles"] = 0
            context["total_routes"] = 0

        # Dormitory stats
        try:
            context["total_rooms"] = Room.objects.count()
        except Exception:
            context["total_rooms"] = 0

        # Leave stats
        try:
            context["pending_leaves"] = LeaveRequest.objects.filter(
                status="pending"
            ).count()
        except Exception:
            context["pending_leaves"] = 0

        # Front desk stats
        try:
            context["today_visitors"] = Visitor.objects.filter(visit_date=today).count()
        except Exception:
            context["today_visitors"] = 0

        # Recent activity logs
        context["recent_activities"] = ActivityLog.objects.select_related(
            "user"
        ).order_by("-created_at")[:15]

        # Recent users
        context["recent_users"] = User.objects.order_by("-date_joined")[:8]

        # New students this month
        context["new_students_month"] = Student.objects.filter(
            created_at__month=today.month, created_at__year=today.year
        ).count()

        # New teachers this month
        context["new_teachers_month"] = Teacher.objects.filter(
            created_at__month=today.month, created_at__year=today.year
        ).count()

        return context


class UserManagementListView(AdminRequiredMixin, ListView):
    """List all users with filtering and search."""

    template_name = "users/user_management_list.html"
    model = User
    context_object_name = "users_list"
    paginate_by = 20

    def get_queryset(self):
        # Using top-level import of User
        qs = User.objects.all().order_by("-date_joined")
        role = self.request.GET.get("role")
        status = self.request.GET.get("status")
        search = self.request.GET.get("search")

        if role and role != "all":
            qs = qs.filter(role=role)
        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)
        if search:
            qs = qs.filter(
                Q(username__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_role"] = self.request.GET.get("role", "all")
        context["current_status"] = self.request.GET.get("status", "all")
        context["search_query"] = self.request.GET.get("search", "")
        return context


class UserCreateView(AdminRequiredMixin, TemplateView):
    """Create a new user."""

    template_name = "users/user_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import AdminUserCreateForm

        context["form"] = AdminUserCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        from .forms import AdminUserCreateForm
        from .models import ActivityLog

        form = AdminUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            ActivityLog.log(
                user=request.user,
                action="create",
                description=f"Created new {user.get_role_display()} user: {user.get_full_name()} ({user.username})",
                category="user_management",
                target_model="User",
                target_id=user.pk,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            messages.success(
                request, f"User '{user.get_full_name()}' created successfully."
            )
            return redirect("users:user_management")
        return render(request, self.template_name, {"form": form})


class UserEditView(AdminRequiredMixin, TemplateView):
    """Edit an existing user."""

    template_name = "users/user_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import AdminUserEditForm
        from .models import User

        user_obj = User.objects.get(pk=kwargs["pk"])
        context["form"] = AdminUserEditForm(instance=user_obj)
        context["edit_user"] = user_obj
        return context

    def post(self, request, *args, **kwargs):
        from .forms import AdminUserEditForm
        from .models import User, ActivityLog

        user_obj = User.objects.get(pk=kwargs["pk"])
        form = AdminUserEditForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            ActivityLog.log(
                user=request.user,
                action="update",
                description=f"Updated user: {user_obj.get_full_name()} ({user_obj.username})",
                category="user_management",
                target_model="User",
                target_id=user_obj.pk,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            messages.success(
                request, f"User '{user_obj.get_full_name()}' updated successfully."
            )
            return redirect("users:user_management")
        return render(
            request, self.template_name, {"form": form, "edit_user": user_obj}
        )


class UserDeleteView(AdminRequiredMixin, TemplateView):
    """Delete a user."""

    template_name = "users/user_delete_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import User

        context["delete_user"] = User.objects.get(pk=kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        from .models import User, ActivityLog

        user_obj = User.objects.get(pk=kwargs["pk"])
        if user_obj == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect("users:user_management")
        name = user_obj.get_full_name()
        username = user_obj.username
        ActivityLog.log(
            user=request.user,
            action="delete",
            description=f"Deleted user: {name} ({username})",
            category="user_management",
            target_model="User",
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        user_obj.delete()
        messages.success(request, f"User '{name}' has been deleted.")
        return redirect("users:user_management")


def toggle_user_active(request, pk):
    """Toggle a user's active status."""
    if not request.user.is_authenticated or not request.user.is_admin_user:
        messages.error(request, "Permission denied.")
        return redirect("users:dashboard")
    from .models import User, ActivityLog

    user_obj = User.objects.get(pk=pk)
    if user_obj == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect("users:user_management")
    user_obj.is_active = not user_obj.is_active
    user_obj.save()
    action_word = "activated" if user_obj.is_active else "deactivated"
    ActivityLog.log(
        user=request.user,
        action="update",
        description=f"{action_word.capitalize()} user: {user_obj.get_full_name()} ({user_obj.username})",
        category="user_management",
        target_model="User",
        target_id=user_obj.pk,
        ip_address=request.META.get("REMOTE_ADDR"),
    )
    messages.success(
        request, f"User '{user_obj.get_full_name()}' has been {action_word}."
    )
    return redirect("users:user_management")


def reset_user_password(request, pk):
    """Reset a user's password."""
    if not request.user.is_authenticated or not request.user.is_admin_user:
        messages.error(request, "Permission denied.")
        return redirect("users:dashboard")
    from .models import User, ActivityLog
    from .forms import AdminPasswordChangeForm

    user_obj = User.objects.get(pk=pk)

    if request.method == "POST":
        form = AdminPasswordChangeForm(request.POST)
        if form.is_valid():
            user_obj.set_password(form.cleaned_data["new_password1"])
            user_obj.save()
            ActivityLog.log(
                user=request.user,
                action="update",
                description=f"Reset password for user: {user_obj.get_full_name()} ({user_obj.username})",
                category="user_management",
                target_model="User",
                target_id=user_obj.pk,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            messages.success(
                request, f"Password updated for '{user_obj.get_full_name()}'."
            )
            return redirect("users:user_management")
    else:
        form = AdminPasswordChangeForm()
    return render(
        request, "users/user_reset_password.html", {"form": form, "edit_user": user_obj}
    )


class ActivityLogListView(AdminRequiredMixin, ListView):
    """View all activity logs."""

    template_name = "users/activity_log_list.html"
    model = ActivityLog
    context_object_name = "activities"
    paginate_by = 30

    def get_queryset(self):
        from .models import ActivityLog

        qs = ActivityLog.objects.select_related("user").order_by("-created_at")
        category = self.request.GET.get("category")
        action = self.request.GET.get("action")
        if category and category != "all":
            qs = qs.filter(category=category)
        if action and action != "all":
            qs = qs.filter(action=action)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.request.GET.get("category", "all")
        context["current_action"] = self.request.GET.get("action", "all")
        return context


def logout_view(request):
    """Logout user and redirect to login page."""
    if request.user.is_authenticated:
        from .models import ActivityLog

        ActivityLog.log(
            user=request.user,
            action="logout",
            description=f"{request.user.get_full_name()} logged out",
            category="auth",
            ip_address=request.META.get("REMOTE_ADDR"),
        )
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("users:login")


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    """View for users to update their own profile picture."""

    template_name = "users/profile_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import UserProfileUpdateForm

        context["form"] = UserProfileUpdateForm(instance=self.request.user)
        context["title"] = "Update Profile Picture"
        return context

    def post(self, request, *args, **kwargs):
        from .forms import UserProfileUpdateForm
        from .models import ActivityLog

        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            ActivityLog.log(
                user=request.user,
                action="update",
                description="Updated profile picture",
                category="profile",
                target_model="User",
                target_id=request.user.pk,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            messages.success(request, "Profile picture updated successfully.")
            return redirect("users:dashboard")
        return render(request, self.template_name, {"form": form})


class AdminRequiredMixin:
    """Mixin to check if user is admin."""

    def test_func(self):
        return self.request.user.is_admin_user


class NonTeachingStaffListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """List all non-teaching staff."""

    model = NonTeachingStaff
    template_name = "users/staff_list.html"
    context_object_name = "staff_list"
    paginate_by = 15

    def get_queryset(self):
        queryset = NonTeachingStaff.objects.select_related("user")
        search = self.request.GET.get("search")
        department = self.request.GET.get("department")

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(staff_id__icontains=search)
                | Q(user__email__icontains=search)
            )
        if department:
            queryset = queryset.filter(department=department)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = NonTeachingStaff.objects.values_list(
            "department", flat=True
        ).distinct()
        return context


class NonTeachingStaffCreateView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    """Create new non-teaching staff."""

    template_name = "users/staff_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = NonTeachingStaffCreationForm()
        return context

    def post(self, request):
        form = NonTeachingStaffCreationForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save()
            ActivityLog.log(
                user=request.user,
                action="create",
                description=f"Created non-teaching staff: {staff.user.get_full_name()}",
                category="staff",
                target_model="NonTeachingStaff",
                target_id=staff.pk,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            messages.success(
                request,
                f"Staff member {staff.user.get_full_name()} created successfully!",
            )
            return redirect("users:staff_list")
        return render(request, self.template_name, {"form": form})


class NonTeachingStaffDetailView(LoginRequiredMixin, DetailView):
    """View non-teaching staff details."""

    model = NonTeachingStaff
    template_name = "users/staff_detail.html"
    context_object_name = "staff"

    def get_queryset(self):
        return NonTeachingStaff.objects.select_related("user")


class NonTeachingStaffUpdateView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    """Update non-teaching staff."""

    template_name = "users/staff_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(NonTeachingStaff, pk=kwargs["pk"])
        context["form"] = NonTeachingStaffForm(instance=staff)
        context["staff"] = staff
        return context

    def post(self, request, pk):
        staff = get_object_or_404(NonTeachingStaff, pk=pk)
        form = NonTeachingStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            ActivityLog.log(
                user=request.user,
                action="update",
                description=f"Updated non-teaching staff: {staff.user.get_full_name()}",
                category="staff",
                target_model="NonTeachingStaff",
                target_id=staff.pk,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            messages.success(request, "Staff member updated successfully!")
            return redirect("users:staff_detail", pk=pk)
        return render(request, self.template_name, {"form": form, "staff": staff})


from django.shortcuts import get_object_or_404
