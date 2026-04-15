from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "finance"

urlpatterns = [
    path("", RedirectView.as_view(url="student-fees/", permanent=False), name="index"),
    path(
        "fee-categories/", views.FeeCategoryListView.as_view(), name="fee_category_list"
    ),
    path(
        "fee-categories/create/",
        views.FeeCategoryCreateView.as_view(),
        name="fee_category_create",
    ),
    path(
        "fee-particulars/",
        views.FeeParticularListView.as_view(),
        name="fee_particular_list",
    ),
    path(
        "fee-particulars/create/",
        views.FeeParticularCreateView.as_view(),
        name="fee_particular_create",
    ),
    path(
        "fee-particulars/<int:pk>/update/",
        views.FeeParticularUpdateView.as_view(),
        name="fee_particular_update",
    ),
    path(
        "fee-particulars/<int:pk>/delete/",
        views.FeeParticularDeleteView.as_view(),
        name="fee_particular_delete",
    ),
    path("fee-groups/", views.FeeGroupListView.as_view(), name="fee_group_list"),
    path(
        "fee-groups/create/",
        views.FeeGroupCreateView.as_view(),
        name="fee_group_create",
    ),
    path(
        "fee-groups/<int:pk>/update/",
        views.FeeGroupUpdateView.as_view(),
        name="fee_group_update",
    ),
    path(
        "fee-groups/<int:pk>/delete/",
        views.FeeGroupDeleteView.as_view(),
        name="fee_group_delete",
    ),
    path("class-fees/", views.ClassFeeListView.as_view(), name="class_fee_list"),
    path(
        "class-fees/create/",
        views.ClassFeeCreateView.as_view(),
        name="class_fee_create",
    ),
    path(
        "class-fees/<int:pk>/update/",
        views.ClassFeeUpdateView.as_view(),
        name="class_fee_update",
    ),
    path(
        "class-fees/<int:pk>/delete/",
        views.ClassFeeDeleteView.as_view(),
        name="class_fee_delete",
    ),
    path(
        "discounts/",
        views.DiscountCategoryListView.as_view(),
        name="discount_category_list",
    ),
    path(
        "discounts/create/",
        views.DiscountCategoryCreateView.as_view(),
        name="discount_category_create",
    ),
    path(
        "discounts/<int:pk>/update/",
        views.DiscountCategoryUpdateView.as_view(),
        name="discount_category_update",
    ),
    path(
        "discounts/<int:pk>/delete/",
        views.DiscountCategoryDeleteView.as_view(),
        name="discount_category_delete",
    ),
    path(
        "student-discounts/",
        views.StudentDiscountListView.as_view(),
        name="student_discount_list",
    ),
    path(
        "student-discounts/create/",
        views.StudentDiscountCreateView.as_view(),
        name="student_discount_create",
    ),
    path(
        "student-discounts/<int:pk>/delete/",
        views.StudentDiscountDeleteView.as_view(),
        name="student_discount_delete",
    ),
    path(
        "fee-structures/",
        views.FeeStructureListView.as_view(),
        name="fee_structure_list",
    ),
    path(
        "fee-structures/create/",
        views.FeeStructureCreateView.as_view(),
        name="fee_structure_create",
    ),
    path("assign-fees/", views.AssignFeesView.as_view(), name="assign_fees"),
    path("generate-fees/", views.GenerateFeesView.as_view(), name="generate_fees"),
    path("student-fees/", views.StudentFeeListView.as_view(), name="student_fee_list"),
    path("payments/", views.PaymentListView.as_view(), name="payment_list"),
    path("payments/create/", views.PaymentCreateView.as_view(), name="payment_create"),
    path("expenses/", views.ExpenseListView.as_view(), name="expense_list"),
    path("expenses/create/", views.ExpenseCreateView.as_view(), name="expense_create"),
    path("report/", views.FinancialReportView.as_view(), name="financial_report"),
]
