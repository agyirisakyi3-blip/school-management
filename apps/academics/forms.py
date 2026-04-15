from django import forms
from .models import Attendance, Exam, ExamSchedule, Result, Timetable


class AttendanceForm(forms.ModelForm):
    """Form for Attendance."""

    class Meta:
        model = Attendance
        fields = ["student", "date", "status", "remarks"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class AttendanceBulkForm(forms.Form):
    """Form for bulk attendance entry."""

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    students = forms.ModelMultipleChoiceField(
        queryset=None, widget=forms.CheckboxSelectMultiple, required=False
    )
    status = forms.ChoiceField(
        choices=Attendance.Status.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
    )


class ExamForm(forms.ModelForm):
    """Form for Exam."""

    class Meta:
        model = Exam
        fields = [
            "name",
            "exam_type",
            "academic_year",
            "start_date",
            "end_date",
            "description",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ExamScheduleForm(forms.ModelForm):
    """Form for Exam Schedule."""

    class Meta:
        model = ExamSchedule
        fields = [
            "exam",
            "subject",
            "assigned_class",
            "exam_date",
            "start_time",
            "end_time",
            "total_marks",
            "passing_marks",
            "venue",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ResultForm(forms.ModelForm):
    """Form for Result."""

    class Meta:
        model = Result
        fields = ["student", "exam_schedule", "marks_obtained", "remarks"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ResultBulkForm(forms.Form):
    """Form for bulk result entry."""

    exam_schedule = forms.ModelChoiceField(
        queryset=ExamSchedule.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    results = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Format: StudentID,Marks\nExample:\nSTU001,85\nSTU002,90",
            }
        )
    )


class TimetableForm(forms.ModelForm):
    """Form for Timetable."""

    class Meta:
        model = Timetable
        fields = [
            "assigned_class",
            "subject",
            "teacher",
            "day",
            "start_time",
            "end_time",
            "venue",
            "academic_year",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
