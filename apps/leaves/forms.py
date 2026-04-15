from django import forms
from .models import LeaveType, LeaveRequest


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = [
            "name",
            "code",
            "description",
            "days_allowed",
            "is_paid",
            "requires_approval",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "days_allowed": forms.NumberInput(attrs={"class": "form-control"}),
            "is_paid": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "requires_approval": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
