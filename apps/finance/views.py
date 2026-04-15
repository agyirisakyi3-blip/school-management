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
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Sum, Q
from .models import (
    FeeCategory,
    FeeParticular,
    FeeGroup,
    FeeGroupParticular,
    ClassFee,
    DiscountCategory,
    StudentDiscount,
    FeeStructure,
    StudentFee,
    Payment,
    Expense,
)
from .forms import (
    FeeCategoryForm,
    FeeParticularForm,
    FeeGroupForm,
    FeeGroupParticularForm,
    ClassFeeForm,
    DiscountCategoryForm,
    StudentDiscountForm,
    FeeStructureForm,
    StudentFeeForm,
    PaymentForm,
    ExpenseForm,
)
from ..students.models import Student, Class, AcademicYear


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class DashboardMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_fees"] = (
            StudentFee.objects.aggregate(total=Sum("amount"))["total"] or 0
        )
        context["total_paid"] = (
            StudentFee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        )
        context["pending_fees"] = context["total_fees"] - context["total_paid"]
        return context


class FeeCategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeeCategory
    template_name = "finance/fee_category_list.html"
    context_object_name = "categories"


class FeeCategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeeCategory
    form_class = FeeCategoryForm
    template_name = "finance/fee_category_form.html"
    success_url = reverse_lazy("finance:fee_category_list")

    def form_valid(self, form):
        messages.success(self.request, "Fee category created successfully.")
        return super().form_valid(form)


class FeeStructureListView(LoginRequiredMixin, ListView):
    model = FeeStructure
    template_name = "finance/fee_structure_list.html"
    context_object_name = "fee_structures"


class FeeStructureCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = "finance/fee_structure_form.html"
    success_url = reverse_lazy("finance:fee_structure_list")

    def form_valid(self, form):
        messages.success(self.request, "Fee structure created successfully.")
        return super().form_valid(form)


class GenerateFeesView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Generate fees for all students based on fee structure."""

    template_name = "finance/generate_fees.html"
    success_url = reverse_lazy("finance:student_fee_list")

    def get(self, request, *args, **kwargs):
        context = {
            "fee_structures": FeeStructure.objects.filter(is_active=True),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        fee_structure_id = request.POST.get("fee_structure")
        if fee_structure_id:
            fee_structure = FeeStructure.objects.get(id=fee_structure_id)
            students = Student.objects.filter(
                current_class=fee_structure.assigned_class, is_active=True
            )
            for student in students:
                StudentFee.objects.update_or_create(
                    student=student,
                    fee_structure=fee_structure,
                    defaults={
                        "amount": fee_structure.amount,
                        "due_date": fee_structure.due_date,
                    },
                )
            messages.success(request, "Fees generated successfully.")
        return redirect(self.success_url)


class StudentFeeListView(LoginRequiredMixin, ListView):
    model = StudentFee
    template_name = "finance/student_fee_list.html"
    context_object_name = "student_fees"
    paginate_by = 50

    def get_queryset(self):
        queryset = StudentFee.objects.select_related(
            "student__user", "fee_structure__category"
        )
        student_id = self.request.GET.get("student")
        status = self.request.GET.get("status")

        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        if status:
            queryset = queryset.filter(status=status)

        if self.request.user.is_student:
            student = Student.objects.filter(user=self.request.user).first()
            if student:
                return queryset.filter(student=student)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_fees"] = (
            StudentFee.objects.aggregate(total=Sum("amount"))["total"] or 0
        )
        context["total_paid"] = (
            StudentFee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        )
        context["pending_fees"] = context["total_fees"] - context["total_paid"]
        context["overdue_count"] = StudentFee.objects.filter(status="overdue").count()
        return context


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "finance/payment_list.html"
    context_object_name = "payments"
    paginate_by = 50

    def get_queryset(self):
        queryset = Payment.objects.select_related(
            "student_fee__student__user", "received_by"
        )
        student_id = self.request.GET.get("student")

        if student_id:
            queryset = queryset.filter(
                student_fee__student__student_id__icontains=student_id
            )

        if self.request.user.is_student:
            student = Student.objects.filter(user=self.request.user).first()
            if student:
                return queryset.filter(student_fee__student=student)

        return queryset


class PaymentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "finance/payment_form.html"
    success_url = reverse_lazy("finance:payment_list")

    def form_valid(self, form):
        from ..communication.utils import send_email

        payment = form.save(commit=False)
        payment.received_by = self.request.user

        student_fee = payment.student_fee
        student_fee.amount_paid += payment.amount
        student_fee.save()

        if student_fee.amount_paid >= student_fee.amount:
            student_fee.status = "paid"
            student_fee.save()
        elif student_fee.amount_paid > 0:
            student_fee.status = "partial"
            student_fee.save()

        if student_fee.student.parent and student_fee.student.parent.email:
            message = f"""
Dear {student_fee.student.parent.get_full_name()},

We have received a payment for {student_fee.student.user.get_full_name()}.

Payment Details:
- Amount: ${payment.amount}
- Category: {student_fee.fee_structure.category.name}
- Payment Date: {payment.payment_date}
- Payment Method: {payment.get_payment_method_display()}

Current Balance: ${student_fee.balance}

Thank you for your payment.

Best regards,
School Management System
            """
            send_email(
                subject=f"Payment Receipt - {student_fee.student.user.get_full_name()}",
                message=message,
                recipient_list=[student_fee.student.parent.email],
            )

        messages.success(self.request, "Payment recorded successfully.")
        return super().form_valid(form)


class ExpenseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Expense
    template_name = "finance/expense_list.html"
    context_object_name = "expenses"

    def get_queryset(self):
        return Expense.objects.order_by("-expense_date")


class ExpenseCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "finance/expense_form.html"
    success_url = reverse_lazy("finance:expense_list")

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, "Expense recorded successfully.")
        return super().form_valid(form)


class FinancialReportView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Financial summary report."""

    model = StudentFee
    template_name = "finance/financial_report.html"
    context_object_name = "fees"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_paid = (
            StudentFee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        )
        total_expenses = Expense.objects.aggregate(total=Sum("amount"))["total"] or 0

        context["total_income"] = total_paid
        context["total_expenses"] = total_expenses
        context["net_balance"] = total_paid - total_expenses
        context["income_by_category"] = list(
            StudentFee.objects.values("fee_structure__category__name").annotate(
                total=Sum("amount_paid")
            )
        )
        context["expenses_by_category"] = list(
            Expense.objects.values("category").annotate(total=Sum("amount"))
        )
        return context


class FeeParticularListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeeParticular
    template_name = "finance/fee_particular_list.html"
    context_object_name = "particulars"
    paginate_by = 30

    def get_queryset(self):
        queryset = FeeParticular.objects.select_related("category")
        search = self.request.GET.get("search")
        category = self.request.GET.get("category")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        if category:
            queryset = queryset.filter(category_id=category)

        return queryset.order_by("category__name", "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = FeeCategory.objects.filter(is_active=True)
        context["search"] = self.request.GET.get("search", "")
        context["category_filter"] = self.request.GET.get("category", "")
        context["total_particulars"] = FeeParticular.objects.count()
        context["active_particulars"] = FeeParticular.objects.filter(
            is_active=True
        ).count()
        return context


class FeeParticularCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeeParticular
    form_class = FeeParticularForm
    template_name = "finance/fee_particular_form.html"
    success_url = reverse_lazy("finance:fee_particular_list")

    def form_valid(self, form):
        messages.success(self.request, "Fee particular created successfully.")
        return super().form_valid(form)


class FeeParticularUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FeeParticular
    form_class = FeeParticularForm
    template_name = "finance/fee_particular_form.html"
    success_url = reverse_lazy("finance:fee_particular_list")

    def form_valid(self, form):
        messages.success(self.request, "Fee particular updated successfully.")
        return super().form_valid(form)


class FeeParticularDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = FeeParticular
    template_name = "finance/fee_particular_confirm_delete.html"
    success_url = reverse_lazy("finance:fee_particular_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Fee particular deleted successfully.")
        return super().delete(request, *args, **kwargs)


class FeeGroupListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeeGroup
    template_name = "finance/fee_group_list.html"
    context_object_name = "fee_groups"

    def get_queryset(self):
        queryset = FeeGroup.objects.select_related("academic_year")
        academic_year = self.request.GET.get("academic_year")

        if academic_year:
            queryset = queryset.filter(academic_year_id=academic_year)

        return queryset.prefetch_related("particulars")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["academic_years"] = AcademicYear.objects.all()
        context["academic_year_filter"] = self.request.GET.get("academic_year", "")
        context["total_groups"] = FeeGroup.objects.count()
        return context


class FeeGroupCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeeGroup
    form_class = FeeGroupForm
    template_name = "finance/fee_group_form.html"
    success_url = reverse_lazy("finance:fee_group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["particulars"] = FeeParticular.objects.filter(is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            fee_group = form.save()
            particular_ids = request.POST.getlist("particulars")
            for pid in particular_ids:
                FeeGroupParticular.objects.create(
                    fee_group=fee_group, particular_id=pid
                )
            messages.success(request, "Fee group created successfully.")
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})

    def form_valid(self, form):
        messages.success(self.request, "Fee group created successfully.")
        return super().form_valid(form)


class FeeGroupUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FeeGroup
    form_class = FeeGroupForm
    template_name = "finance/fee_group_form.html"
    success_url = reverse_lazy("finance:fee_group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["particulars"] = FeeParticular.objects.filter(is_active=True)
        context["selected_particulars"] = list(
            self.object.feegroupparticular_set.values_list("particular_id", flat=True)
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, instance=self.object)
        if form.is_valid():
            fee_group = form.save()
            FeeGroupParticular.objects.filter(fee_group=fee_group).delete()
            particular_ids = request.POST.getlist("particulars")
            for pid in particular_ids:
                FeeGroupParticular.objects.create(
                    fee_group=fee_group, particular_id=pid
                )
            messages.success(request, "Fee group updated successfully.")
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})

    def form_valid(self, form):
        messages.success(self.request, "Fee group updated successfully.")
        return super().form_valid(form)


class FeeGroupDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = FeeGroup
    template_name = "finance/fee_group_confirm_delete.html"
    success_url = reverse_lazy("finance:fee_group_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Fee group deleted successfully.")
        return super().delete(request, *args, **kwargs)


class ClassFeeListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ClassFee
    template_name = "finance/class_fee_list.html"
    context_object_name = "class_fees"

    def get_queryset(self):
        queryset = ClassFee.objects.select_related(
            "assigned_class", "fee_group"
        ).prefetch_related("fee_group__particulars")
        class_filter = self.request.GET.get("class")
        academic_year = self.request.GET.get("academic_year")

        if class_filter:
            queryset = queryset.filter(assigned_class_id=class_filter)
        if academic_year:
            queryset = queryset.filter(fee_group__academic_year_id=academic_year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classes"] = Class.objects.all()
        context["academic_years"] = AcademicYear.objects.all()
        context["class_filter"] = self.request.GET.get("class", "")
        context["academic_year_filter"] = self.request.GET.get("academic_year", "")
        context["total_class_fees"] = ClassFee.objects.count()
        return context


class ClassFeeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ClassFee
    form_class = ClassFeeForm
    template_name = "finance/class_fee_form.html"
    success_url = reverse_lazy("finance:class_fee_list")

    def form_valid(self, form):
        messages.success(self.request, "Class fee assigned successfully.")
        return super().form_valid(form)


class ClassFeeUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ClassFee
    form_class = ClassFeeForm
    template_name = "finance/class_fee_form.html"
    success_url = reverse_lazy("finance:class_fee_list")

    def form_valid(self, form):
        messages.success(self.request, "Class fee updated successfully.")
        return super().form_valid(form)


class ClassFeeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ClassFee
    template_name = "finance/class_fee_confirm_delete.html"
    success_url = reverse_lazy("finance:class_fee_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Class fee removed successfully.")
        return super().delete(request, *args, **kwargs)


class DiscountCategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = DiscountCategory
    template_name = "finance/discount_category_list.html"
    context_object_name = "discounts"

    def get_queryset(self):
        return DiscountCategory.objects.order_by("name")


class DiscountCategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = DiscountCategory
    form_class = DiscountCategoryForm
    template_name = "finance/discount_category_form.html"
    success_url = reverse_lazy("finance:discount_category_list")

    def form_valid(self, form):
        messages.success(self.request, "Discount category created successfully.")
        return super().form_valid(form)


class DiscountCategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = DiscountCategory
    form_class = DiscountCategoryForm
    template_name = "finance/discount_category_form.html"
    success_url = reverse_lazy("finance:discount_category_list")

    def form_valid(self, form):
        messages.success(self.request, "Discount category updated successfully.")
        return super().form_valid(form)


class DiscountCategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = DiscountCategory
    template_name = "finance/discount_category_confirm_delete.html"
    success_url = reverse_lazy("finance:discount_category_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Discount category deleted successfully.")
        return super().delete(request, *args, **kwargs)


class StudentDiscountListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = StudentDiscount
    template_name = "finance/student_discount_list.html"
    context_object_name = "student_discounts"

    def get_queryset(self):
        queryset = StudentDiscount.objects.select_related(
            "student__user", "discount_category"
        )
        student_id = self.request.GET.get("student")
        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["discount_categories"] = DiscountCategory.objects.filter(is_active=True)
        return context


class StudentDiscountCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = StudentDiscount
    form_class = StudentDiscountForm
    template_name = "finance/student_discount_form.html"
    success_url = reverse_lazy("finance:student_discount_list")

    def form_valid(self, form):
        messages.success(self.request, "Student discount assigned successfully.")
        return super().form_valid(form)


class StudentDiscountDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = StudentDiscount
    template_name = "finance/student_discount_confirm_delete.html"
    success_url = reverse_lazy("finance:student_discount_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Student discount removed successfully.")
        return super().delete(request, *args, **kwargs)


class AssignFeesView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Assign fees to all students in a class."""

    template_name = "finance/assign_fees.html"

    def get(self, request):
        context = {
            "classes": Class.objects.filter(is_active=True)
            if hasattr(Class, "is_active")
            else Class.objects.all(),
            "fee_groups": FeeGroup.objects.filter(is_active=True),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        class_id = request.POST.get("class_id")
        fee_group_id = request.POST.get("fee_group_id")

        if not class_id or not fee_group_id:
            messages.error(request, "Please select both class and fee group.")
            return redirect("finance:assign_fees")

        try:
            class_fee = ClassFee.objects.get_or_create(
                assigned_class_id=class_id, fee_group_id=fee_group_id
            )[0]

            class_obj = Class.objects.get(id=class_id)
            students = Student.objects.filter(current_class=class_obj, is_active=True)
            created_count = 0

            for student in students:
                fee_group = class_fee.fee_group
                for fg_particular in fee_group.feegroupparticular_set.all():
                    particular = fg_particular.particular
                    amount = fg_particular.get_amount()

                    if particular.frequency == "monthly":
                        from datetime import date
                        from dateutil.relativedelta import relativedelta

                        current = date.today()
                        for month in range(12):
                            month_date = current + relativedelta(months=month)
                            StudentFee.objects.update_or_create(
                                student=student,
                                fee_structure=FeeStructure.objects.get_or_create(
                                    category=particular.category,
                                    assigned_class=class_obj,
                                    academic_year=fee_group.academic_year,
                                    defaults={
                                        "amount": amount,
                                        "due_date": month_date.replace(day=5),
                                    },
                                )[0],
                                defaults={
                                    "amount": amount,
                                    "due_date": month_date.replace(day=5),
                                },
                            )
                            created_count += 1
                    else:
                        StudentFee.objects.update_or_create(
                            student=student,
                            fee_structure=FeeStructure.objects.get_or_create(
                                category=particular.category,
                                assigned_class=class_obj,
                                academic_year=fee_group.academic_year,
                                defaults={
                                    "amount": amount,
                                    "due_date": date(date.today().year, 12, 31),
                                },
                            )[0],
                            defaults={
                                "amount": amount,
                                "due_date": date(date.today().year, 12, 31),
                            },
                        )
                        created_count += 1

            messages.success(
                request,
                f"Fees assigned to {students.count()} students. {created_count} fee records created.",
            )
        except Exception as e:
            messages.error(request, f"Error assigning fees: {str(e)}")

        return redirect("finance:student_fee_list")
