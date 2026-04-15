from django import forms
from .models import Homework, HomeworkSubmission


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = [
            "title",
            "description",
            "subject",
            "class_obj",
            "teacher",
            "due_date",
            "priority",
            "attachments",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "class_obj": forms.Select(attrs={"class": "form-select"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "attachments": forms.FileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ["submission_text", "attachment"]
        widgets = {
            "submission_text": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "attachment": forms.FileInput(attrs={"class": "form-control"}),
        }


class HomeworkEvaluationForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ["status", "feedback", "marks"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "feedback": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "marks": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }
