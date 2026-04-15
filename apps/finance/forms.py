from django import forms
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


class FeeCategoryForm(forms.ModelForm):
    """Form for Fee Category."""

    class Meta:
        model = FeeCategory
        fields = ["name", "code", "category_type", "description", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["is_active"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class FeeParticularForm(forms.ModelForm):
    """Form for Fee Particular."""

    class Meta:
        model = FeeParticular
        fields = [
            "category",
            "name",
            "code",
            "description",
            "amount",
            "frequency",
            "is_optional",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["is_optional", "is_active"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class FeeGroupForm(forms.ModelForm):
    """Form for Fee Group."""

    class Meta:
        model = FeeGroup
        fields = ["name", "code", "academic_year", "description", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({"class": "form-control"})


class FeeGroupParticularForm(forms.ModelForm):
    """Form for Fee Group Particular."""

    class Meta:
        model = FeeGroupParticular
        fields = ["particular", "custom_amount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["particular"].widget.attrs.update({"class": "form-control select2"})
        self.fields["custom_amount"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Leave blank to use default amount",
            }
        )


class ClassFeeForm(forms.ModelForm):
    """Form for Class Fee."""

    class Meta:
        model = ClassFee
        fields = ["fee_group", "amount_override", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({"class": "form-control"})


class DiscountCategoryForm(forms.ModelForm):
    """Form for Discount Category."""

    class Meta:
        model = DiscountCategory
        fields = [
            "name",
            "code",
            "discount_type",
            "value",
            "max_amount",
            "description",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["is_active"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class StudentDiscountForm(forms.ModelForm):
    """Form for Student Discount."""

    class Meta:
        model = StudentDiscount
        fields = ["discount_category", "reason", "start_date", "end_date", "is_active"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["is_active"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class FeeStructureForm(forms.ModelForm):
    """Form for Fee Structure."""

    class Meta:
        model = FeeStructure
        fields = [
            "category",
            "assigned_class",
            "academic_year",
            "amount",
            "due_date",
            "is_active",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({"class": "form-control"})


class StudentFeeForm(forms.ModelForm):
    """Form for Student Fee."""

    class Meta:
        model = StudentFee
        fields = ["student", "fee_structure", "amount", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class PaymentForm(forms.ModelForm):
    """Form for Payment."""

    class Meta:
        model = Payment
        fields = [
            "student_fee",
            "amount",
            "payment_date",
            "payment_method",
            "transaction_id",
            "remarks",
        ]
        widgets = {
            "payment_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class PaymentCreateForm(forms.ModelForm):
    """Form for creating payment with student selection."""

    class Meta:
        model = Payment
        fields = [
            "amount",
            "payment_date",
            "payment_method",
            "transaction_id",
            "remarks",
        ]
        widgets = {
            "payment_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ExpenseForm(forms.ModelForm):
    """Form for Expense."""

    class Meta:
        model = Expense
        fields = [
            "title",
            "category",
            "amount",
            "expense_date",
            "description",
            "receipt_number",
        ]
        widgets = {
            "expense_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
