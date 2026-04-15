from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher, TeacherSubject

User = get_user_model()


class TeacherForm(forms.ModelForm):
    """Form for Teacher."""

    class Meta:
        model = Teacher
        fields = [
            "employee_id",
            "join_date",
            "qualification",
            "experience_years",
            "specialization",
            "department",
            "salary",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class TeacherCreationForm(forms.ModelForm):
    """Form for creating a teacher with user account."""

    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = [
            "employee_id",
            "email",
            "first_name",
            "last_name",
            "password",
            "join_date",
            "qualification",
            "experience_years",
            "specialization",
            "department",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["employee_id"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role="teacher",
        )
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher


class TeacherSubjectForm(forms.ModelForm):
    """Form for Teacher Subject Assignment."""

    class Meta:
        model = TeacherSubject
        fields = ["teacher", "subject", "assigned_class", "academic_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["teacher"].queryset = Teacher.objects.filter(is_active=True)
