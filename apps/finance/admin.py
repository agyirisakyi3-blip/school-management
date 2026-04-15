from django.contrib import admin
from .models import FeeCategory, FeeStructure, StudentFee, Payment, Expense


@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "assigned_class",
        "academic_year",
        "amount",
        "due_date",
        "is_active",
    ]
    list_filter = ["category", "assigned_class", "academic_year", "is_active"]
    search_fields = ["category__name", "assigned_class__name"]


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "fee_structure",
        "amount",
        "amount_paid",
        "status",
        "due_date",
    ]
    list_filter = ["status", "fee_structure__category", "due_date"]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__student_id",
    ]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "student_fee",
        "amount",
        "payment_date",
        "payment_method",
        "received_by",
    ]
    list_filter = ["payment_method", "payment_date"]
    search_fields = [
        "student_fee__student__user__first_name",
        "student_fee__student__student_id",
    ]
    readonly_fields = ["created_at"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "amount", "expense_date", "recorded_by"]
    list_filter = ["category", "expense_date"]
    search_fields = ["title", "receipt_number"]
    readonly_fields = ["created_at"]
