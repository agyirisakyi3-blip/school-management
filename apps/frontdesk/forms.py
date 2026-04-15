from django import forms
from .models import AdmissionQuery, Visitor, Complaint


class AdmissionQueryForm(forms.ModelForm):
    class Meta:
        model = AdmissionQuery
        fields = [
            "name",
            "email",
            "phone",
            "address",
            "student_name",
            "class_interested",
            "message",
            "status",
            "follow_up_date",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "student_name": forms.TextInput(attrs={"class": "form-control"}),
            "class_interested": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "follow_up_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            "name",
            "phone",
            "email",
            "address",
            "purpose",
            "person_to_meet",
            "remarks",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "purpose": forms.TextInput(attrs={"class": "form-control"}),
            "person_to_meet": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            "complaint_type",
            "complainant_name",
            "complainant_email",
            "complainant_phone",
            "subject",
            "description",
            "priority",
        ]
        widgets = {
            "complaint_type": forms.Select(attrs={"class": "form-select"}),
            "complainant_name": forms.TextInput(attrs={"class": "form-control"}),
            "complainant_email": forms.EmailInput(attrs={"class": "form-control"}),
            "complainant_phone": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }


class ComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            "status",
            "assigned_to",
            "resolution",
        ]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "assigned_to": forms.TextInput(attrs={"class": "form-control"}),
            "resolution": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
