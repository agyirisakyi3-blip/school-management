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
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import calendar as cal_module
from .models import (
    Attendance,
    Exam,
    ExamSchedule,
    Result,
    Timetable,
    Question,
    StudentExam,
    StudentAnswer,
)
from .forms import (
    AttendanceForm,
    AttendanceBulkForm,
    ExamForm,
    ExamScheduleForm,
    ResultForm,
    TimetableForm,
)
from ..students.models import Student, Class


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user or self.request.user.is_teacher

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "academics/attendance_list.html"
    context_object_name = "attendances"
    paginate_by = 50

    def get_queryset(self):
        queryset = Attendance.objects.select_related("student__user", "marked_by")
        date = self.request.GET.get("date")
        student_id = self.request.GET.get("student")
        status = self.request.GET.get("status")

        if date:
            queryset = queryset.filter(date=date)
        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        if status:
            queryset = queryset.filter(status=status)

        if self.request.user.is_student:
            student = Student.objects.filter(user=self.request.user).first()
            if student:
                return queryset.filter(student=student)

        if self.request.user.is_teacher:
            teacher_class = Class.objects.filter(
                class_teacher=self.request.user
            ).first()
            if teacher_class:
                return queryset.filter(student__current_class=teacher_class)

        return queryset.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["present_count"] = queryset.filter(status="present").count()
        context["absent_count"] = queryset.filter(status="absent").count()
        context["late_count"] = queryset.filter(status="late").count()
        total = queryset.count()
        context["attendance_rate"] = (
            round((context["present_count"] / total) * 100, 1) if total > 0 else 0
        )
        return context


class AttendanceCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "academics/attendance_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.request.GET.get("year", datetime.now().year))
        month = int(self.request.GET.get("month", datetime.now().month))
        class_id = self.request.GET.get("class_id")

        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, cal_module.monthrange(year, month)[1])

        queryset = Attendance.objects.filter(
            date__gte=first_day.date(), date__lte=last_day.date()
        )

        if class_id:
            queryset = queryset.filter(student__current_class_id=class_id)
        elif self.request.user.is_teacher:
            teacher_class = Class.objects.filter(
                class_teacher=self.request.user
            ).first()
            if teacher_class:
                queryset = queryset.filter(student__current_class=teacher_class)
        elif self.request.user.is_student:
            student = Student.objects.filter(user=self.request.user).first()
            if student:
                queryset = queryset.filter(student=student)

        attendance_by_date = {}
        for att in queryset:
            date_str = att.date.strftime("%Y-%m-%d")
            if date_str not in attendance_by_date:
                attendance_by_date[date_str] = {"present": 0, "absent": 0, "late": 0}
            attendance_by_date[date_str][att.status] += 1

        context["attendance_data"] = attendance_by_date
        context["year"] = year
        context["month"] = month
        context["month_name"] = cal_module.month_name[month]
        context["classes"] = Class.objects.all()
        context["selected_class"] = class_id
        context["prev_month"] = (month - 1) if month > 1 else 12
        context["prev_year"] = year if month > 1 else year - 1
        context["next_month"] = (month + 1) if month < 12 else 1
        context["next_year"] = year if month < 12 else year + 1
        context["calendar_days"] = self.get_calendar_days(year, month)
        return context

    def get_calendar_days(self, year, month):
        cal = cal_module.Calendar(firstweekday=0)
        days = []
        for week in cal.monthdayscalendar(year, month):
            week_days = []
            for day in week:
                if day == 0:
                    week_days.append({"day": None, "in_month": False})
                else:
                    week_days.append({"day": day, "in_month": True})
            days.append(week_days)
        return days


class AttendanceCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "academics/attendance_form.html"
    success_url = reverse_lazy("academics:attendance_list")

    def form_valid(self, form):
        form.instance.marked_by = self.request.user
        messages.success(self.request, "Attendance marked successfully.")
        return super().form_valid(form)


class AttendanceBulkCreateView(LoginRequiredMixin, TeacherRequiredMixin, View):
    template_name = "academics/attendance_bulk_form.html"
    success_url = reverse_lazy("academics:attendance_list")

    def get(self, request, *args, **kwargs):
        form = AttendanceBulkForm(initial={"date": request.GET.get("date")})
        class_id = request.GET.get("class_id")
        if class_id:
            students = Student.objects.filter(current_class_id=class_id, is_active=True)
            form.fields["students"].queryset = students
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = AttendanceBulkForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            status = form.cleaned_data["status"]
            remarks = form.cleaned_data["remarks"]
            students = form.cleaned_data["students"]

            for student in students:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={
                        "status": status,
                        "remarks": remarks,
                        "marked_by": request.user,
                    },
                )

            messages.success(request, "Attendance marked successfully.")
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = "academics/exam_list.html"
    context_object_name = "exams"

    def get_queryset(self):
        return (
            Exam.objects.select_related("academic_year")
            .prefetch_related("exam_schedules")
            .order_by("-start_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now().date()
        context["upcoming_exams"] = Exam.objects.filter(
            start_date__gt=today, is_active=True
        ).count()
        context["ongoing_exams"] = Exam.objects.filter(
            start_date__lte=today, end_date__gte=today, is_active=True
        ).count()
        context["completed_exams"] = Exam.objects.filter(
            end_date__lt=today, is_active=True
        ).count()
        return context


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "academics/exam_detail.html"
    context_object_name = "exam"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedules = self.object.exam_schedules.select_related(
            "subject", "assigned_class"
        )
        context["schedules"] = schedules
        context["result_count"] = Result.objects.filter(
            exam_schedule__exam=self.object
        ).count()
        context["unique_students"] = (
            Result.objects.filter(exam_schedule__exam=self.object)
            .values("student")
            .distinct()
            .count()
        )
        return context


class ExamCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = "academics/exam_form.html"
    success_url = reverse_lazy("academics:exam_list")

    def form_valid(self, form):
        messages.success(self.request, "Exam created successfully.")
        return super().form_valid(form)


class ExamScheduleCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = ExamSchedule
    form_class = ExamScheduleForm
    template_name = "academics/exam_schedule_form.html"
    success_url = reverse_lazy("academics:exam_list")

    def form_valid(self, form):
        messages.success(self.request, "Exam schedule created successfully.")
        return super().form_valid(form)


class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = "academics/result_list.html"
    context_object_name = "results"
    paginate_by = 50

    def get_queryset(self):
        queryset = Result.objects.select_related(
            "student__user", "exam_schedule__subject"
        )

        student_id = self.request.GET.get("student")
        exam_id = self.request.GET.get("exam")

        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        if exam_id:
            queryset = queryset.filter(exam_schedule__exam_id=exam_id)

        if self.request.user.is_student:
            student = Student.objects.filter(user=self.request.user).first()
            if student:
                return queryset.filter(student=student)

        return queryset


class ResultCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Result
    form_class = ResultForm
    template_name = "academics/result_form.html"
    success_url = reverse_lazy("academics:result_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Result added successfully.")
        return super().form_valid(form)


class TimetableListView(LoginRequiredMixin, ListView):
    model = Timetable
    template_name = "academics/timetable_list.html"
    context_object_name = "timetables"

    def get_queryset(self):
        queryset = Timetable.objects.select_related(
            "assigned_class", "subject", "teacher"
        )
        class_id = self.request.GET.get("class_id")

        if class_id:
            queryset = queryset.filter(assigned_class_id=class_id)

        if self.request.user.is_student:
            student = Student.objects.filter(user=self.request.user).first()
            if student and student.current_class:
                queryset = queryset.filter(assigned_class=student.current_class)

        return queryset.order_by("day", "start_time")


class TimetableCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "academics/timetable_form.html"
    success_url = reverse_lazy("academics:timetable_list")

    def form_valid(self, form):
        messages.success(self.request, "Timetable entry added successfully.")
        return super().form_valid(form)


class StudentReportView(LoginRequiredMixin, DetailView):
    """Generate student report card."""

    model = Student
    template_name = "academics/student_report.html"
    context_object_name = "student"

    def get_queryset(self):
        user = self.request.user
        queryset = Student.objects.select_related("user", "current_class")

        if user.is_admin_user:
            return queryset
        if user.is_student:
            return queryset.filter(user=user)
        if user.is_teacher:
            # Teachers can see reports for students in classes they teach
            teacher_classes = Class.objects.filter(class_teacher=user)
            return queryset.filter(current_class__in=teacher_classes)
        if user.is_parent:
            # Parents can see their wards' reports
            return queryset.filter(parent=user)

        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context["results"] = Result.objects.filter(student=student).select_related(
            "exam_schedule__subject", "exam_schedule__exam"
        )
        context["attendance_summary"] = Attendance.objects.filter(student=student)

        total_att = context["attendance_summary"].count()
        present_att = context["attendance_summary"].filter(status="present").count()
        context["attendance_pct"] = (
            round((present_att / total_att) * 100, 1) if total_att > 0 else 0
        )

        return context


class StudentReportPDFView(LoginRequiredMixin, DetailView):
    """Generate PDF report card for student."""

    model = Student
    context_object_name = "student"

    def get_queryset(self):
        user = self.request.user
        queryset = Student.objects.all()

        if user.is_admin_user:
            return queryset
        if user.is_student:
            return queryset.filter(user=user)
        if user.is_teacher:
            teacher_classes = Class.objects.filter(class_teacher=user)
            return queryset.filter(current_class__in=teacher_classes)
        if user.is_parent:
            return queryset.filter(parent=user)

        return queryset.none()

    def get(self, request, *args, **kwargs):
        from django.http import HttpResponse
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch, cm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Table,
            TableStyle,
            Paragraph,
            Spacer,
            Image,
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from io import BytesIO

        student = self.get_object()
        results = Result.objects.filter(student=student).select_related(
            "exam_schedule__subject", "exam_schedule__exam"
        )
        attendance = Attendance.objects.filter(student=student)
        total_att = attendance.count()
        present_att = attendance.filter(status="present").count()
        attendance_pct = (
            round((present_att / total_att) * 100, 1) if total_att > 0 else 0
        )

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=20,
        )
        heading_style = ParagraphStyle(
            "CustomHeading", parent=styles["Heading2"], fontSize=14, spaceAfter=10
        )

        elements = []
        elements.append(Paragraph("Student Report Card", title_style))
        elements.append(Spacer(1, 20))

        student_data = [
            [
                "Student Name:",
                student.user.get_full_name(),
                "Student ID:",
                student.student_id,
            ],
            [
                "Class:",
                student.current_class.name if student.current_class else "-",
                "Roll No:",
                student.roll_number or "-",
            ],
            [
                "Gender:",
                student.get_gender_display(),
                "Attendance:",
                f"{attendance_pct}%",
            ],
            [
                "Parent/Guardian:",
                student.guardian_name,
                "Phone:",
                student.guardian_phone,
            ],
        ]

        student_table = Table(
            student_data, colWidths=[1.5 * inch, 2 * inch, 1.5 * inch, 2 * inch]
        )
        student_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.Color(0.95, 0.95, 0.95)),
                    ("BACKGROUND", (2, 0), (2, -1), colors.Color(0.95, 0.95, 0.95)),
                ]
            )
        )
        elements.append(student_table)
        elements.append(Spacer(1, 20))

        if results:
            elements.append(Paragraph("Academic Results", heading_style))

            result_data = [["Subject", "Exam", "Marks", "Max Marks", "Status"]]
            for result in results:
                result_data.append(
                    [
                        result.exam_schedule.subject.name,
                        result.exam_schedule.exam.name,
                        str(result.marks_obtained),
                        str(result.exam_schedule.subject.passing_marks),
                        "Pass"
                        if result.marks_obtained
                        >= result.exam_schedule.subject.passing_marks
                        else "Fail",
                    ]
                )

            result_table = Table(
                result_data,
                colWidths=[2 * inch, 1.5 * inch, 1 * inch, 1 * inch, 1 * inch],
            )
            result_table.setStyle(
                TableStyle(
                    [
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 9),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.4, 0.6)),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.Color(0.95, 0.95, 0.95)],
                        ),
                    ]
                )
            )
            elements.append(result_table)

        elements.append(Spacer(1, 30))

        summary_data = [
            ["Total Classes", "Classes Attended", "Attendance %"],
            [str(total_att), str(present_att), f"{attendance_pct}%"],
        ]
        summary_table = Table(summary_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.1, 0.5, 0.3)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        elements.append(summary_table)

        elements.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey,
        )
        elements.append(
            Paragraph(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                footer_style,
            )
        )
        elements.append(
            Paragraph(
                "This is a computer-generated document. No signature is required.",
                footer_style,
            )
        )

        doc.build(elements)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="report_{student.student_id}.pdf"'
        )
        response.write(buffer.getvalue())
        buffer.close()
        return response


class OnlineExamListView(LoginRequiredMixin, ListView):
    """List available online exams for students."""

    model = ExamSchedule
    template_name = "academics/online_exam_list.html"
    context_object_name = "exams"

    def get_queryset(self):
        student = self.request.user.student_profile
        if not student:
            return ExamSchedule.objects.none()
        from django.utils import timezone

        now = timezone.now()
        return ExamSchedule.objects.filter(
            is_online=True,
            exam__is_active=True,
            assigned_class=student.current_class,
        ).select_related("exam", "subject", "assigned_class")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student_profile
        if not student:
            return context
        context["completed_exams"] = StudentExam.objects.filter(
            student=student, is_submitted=True
        ).values_list("exam_schedule_id", flat=True)
        return context


class OnlineExamView(LoginRequiredMixin, View):
    """Take an online exam."""

    def get(self, request, pk):
        exam_schedule = get_object_or_404(ExamSchedule, pk=pk)
        student = request.user.student_profile

        # Check if already started
        student_exam, created = StudentExam.objects.get_or_create(
            student=student,
            exam_schedule=exam_schedule,
            defaults={"is_submitted": False},
        )

        if student_exam.is_submitted:
            messages.error(request, "Exam already submitted.")
            return redirect("academics:online_exam_list")

        # Check time remaining
        if student_exam.time_remaining <= 0:
            student_exam.is_submitted = True
            student_exam.save()
            messages.error(request, "Time expired for this exam.")
            return redirect("academics:online_exam_list")

        questions = exam_schedule.questions.all().order_by("order")
        answers = {a.question_id: a.answer for a in student_exam.answers.all()}

        context = {
            "exam_schedule": exam_schedule,
            "student_exam": student_exam,
            "questions": questions,
            "answers": answers,
            "time_remaining": student_exam.time_remaining,
        }
        return render(request, "academics/online_exam.html", context)

    def post(self, request, pk):
        exam_schedule = get_object_or_404(ExamSchedule, pk=pk)
        student = request.user.student_profile

        student_exam = get_object_or_404(
            StudentExam,
            student=student,
            exam_schedule=exam_schedule,
            is_submitted=False,
        )

        # Save answers
        questions = exam_schedule.questions.all()
        total_marks = 0

        for question in questions:
            answer = request.POST.get(f"question_{question.id}", "")

            student_answer, _ = StudentAnswer.objects.update_or_create(
                student_exam=student_exam,
                question=question,
                defaults={"answer": answer},
            )

            # Auto-evaluate for multiple choice and true/false
            if question.question_type in ["multiple_choice", "true_false"]:
                is_correct = (
                    answer.strip().lower() == question.correct_answer.strip().lower()
                )
                student_answer.is_correct = is_correct
                student_answer.marks_obtained = question.marks if is_correct else 0
                student_answer.evaluated_at = timezone.now()
                student_answer.save()
                total_marks += student_answer.marks_obtained or 0

        # Calculate percentage
        if exam_schedule.total_marks > 0:
            percentage = (total_marks / exam_schedule.total_marks) * 100
        else:
            percentage = 0

        # Submit exam
        student_exam.is_submitted = True
        student_exam.submitted_at = timezone.now()
        student_exam.score = total_marks
        student_exam.percentage = percentage
        student_exam.save()

        messages.success(
            request,
            f"Exam submitted! Your score: {total_marks}/{exam_schedule.total_marks} ({percentage:.1f}%)",
        )
        return redirect("academics:online_exam_list")


class ExamResultView(LoginRequiredMixin, DetailView):
    """View exam result after submission."""

    model = StudentExam
    template_name = "academics/exam_result.html"
    context_object_name = "student_exam"

    def get_queryset(self):
        return StudentExam.objects.filter(
            student=self.request.user.student_profile, is_submitted=True
        ).select_related("exam_schedule__exam", "exam_schedule__subject")
