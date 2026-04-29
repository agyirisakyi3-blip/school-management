from django import forms
from django.contrib.auth import get_user_model
from .models import Student, Class, Subject, AcademicYear, AdmissionApplication

User = get_user_model()

GENDER_CHOICES = [
    ("", "Select Gender"),
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]

BLOOD_GROUP_CHOICES = [
    ("", "Select Blood Group"),
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]

RELIGION_CHOICES = [
    ("", "Select Religion"),
    ("hindu", "Hindu"),
    ("muslim", "Muslim"),
    ("christian", "Christian"),
    ("sikh", "Sikh"),
    ("buddhist", "Buddhist"),
    ("jain", "Jain"),
    ("other", "Other"),
]

RELATION_CHOICES = [
    ("", "Select Relation"),
    ("father", "Father"),
    ("mother", "Mother"),
    ("brother", "Brother"),
    ("sister", "Sister"),
    ("grandfather", "Grandfather"),
    ("grandmother", "Grandmother"),
    ("uncle", "Uncle"),
    ("aunt", "Aunt"),
    ("other", "Other"),
]


class AcademicYearForm(forms.ModelForm):
    """Form for Academic Year."""

    class Meta:
        model = AcademicYear
        fields = ["name", "start_date", "end_date", "is_current"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        if self.instance and self.instance.is_current:
            self.fields["is_current"].disabled = True


class ClassForm(forms.ModelForm):
    """Form for Class."""

    class Meta:
        model = Class
        fields = ["name", "code", "academic_year", "class_teacher", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["class_teacher"].queryset = User.objects.filter(role="teacher")


class SubjectForm(forms.ModelForm):
    """Form for Subject."""

    class Meta:
        model = Subject
        fields = ["name", "code", "classes", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class StudentForm(forms.ModelForm):
    """Form for Student."""

    first_name = forms.CharField(max_length=150, label="First Name", required=True)
    last_name = forms.CharField(max_length=150, label="Last Name", required=True)
    email = forms.EmailField(label="Email", required=False)
    date_of_birth = forms.DateField(
        label="Date of Birth",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, required=False)
    blood_group = forms.ChoiceField(
        label="Blood Group", choices=BLOOD_GROUP_CHOICES, required=False
    )
    religion = forms.ChoiceField(
        label="Religion", choices=RELIGION_CHOICES, required=False
    )
    phone = forms.CharField(max_length=20, label="Phone", required=False)
    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2}), label="Address", required=False
    )
    profile_picture = forms.ImageField(label="Profile Picture", required=False)

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "gender",
            "blood_group",
            "religion",
            "phone",
            "address",
            "profile_picture",
            "admission_date",
            "current_class",
            "roll_number",
            "father_name",
            "mother_name",
            "guardian_name",
            "guardian_relation",
            "guardian_phone",
            "previous_school",
            "aadhar_number",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email
            self.fields["phone"].initial = self.instance.user.phone
            self.fields["date_of_birth"].initial = self.instance.user.date_of_birth
            self.fields["gender"].initial = self.instance.user.gender
            self.fields["blood_group"].initial = self.instance.user.blood_group
            self.fields["address"].initial = self.instance.user.address
            try:
                self.fields[
                    "profile_picture"
                ].initial = self.instance.user.profile_picture
            except:
                pass

        for field in self.fields:
            if field not in ["is_active"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        student = super().save(commit=False)

        if student.user:
            student.user.first_name = self.cleaned_data["first_name"]
            student.user.last_name = self.cleaned_data["last_name"]
            student.user.email = self.cleaned_data.get("email", "")
            student.user.phone = self.cleaned_data.get("phone", "")
            student.user.date_of_birth = self.cleaned_data.get("date_of_birth")
            student.user.gender = self.cleaned_data.get("gender", "")
            student.user.blood_group = self.cleaned_data.get("blood_group", "")
            student.user.address = self.cleaned_data.get("address", "")
            if self.cleaned_data.get("profile_picture"):
                student.user.profile_picture = self.cleaned_data["profile_picture"]
            if commit:
                student.user.save()

        if commit:
            student.save()

        return student


class StudentCreationForm(forms.ModelForm):
    """Form for creating a student with user account."""

    first_name = forms.CharField(max_length=150, label="First Name")
    last_name = forms.CharField(max_length=150, label="Last Name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    date_of_birth = forms.DateField(
        label="Date of Birth",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, required=False)
    blood_group = forms.ChoiceField(
        label="Blood Group", choices=BLOOD_GROUP_CHOICES, required=False
    )
    religion = forms.ChoiceField(
        label="Religion", choices=RELIGION_CHOICES, required=False
    )
    guardian_relation = forms.ChoiceField(
        label="Guardian Relation", choices=RELATION_CHOICES, required=False
    )
    profile_picture = forms.ImageField(label="Profile Picture", required=False)
    admission_date = forms.DateField(
        label="Admission Date",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "profile_picture",
            "admission_date",
            "current_class",
            "roll_number",
            "father_name",
            "mother_name",
            "guardian_name",
            "guardian_relation",
            "guardian_phone",
            "previous_school",
            "aadhar_number",
            "date_of_birth",
            "gender",
            "blood_group",
            "religion",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["guardian_relation"].required = True

    def clean_student_id(self):
        last_student = Student.objects.order_by("-id").first()
        if last_student and last_student.student_id:
            try:
                num = int(last_student.student_id.replace("STU", ""))
                student_id = f"STU{str(num + 1).zfill(5)}"
            except:
                student_id = "STU00001"
        else:
            student_id = "STU00001"
        return student_id

    def save(self, commit=True):
        student_id = self.clean_student_id()

        base_username = student_id.replace(" ", "").lower()
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=self.cleaned_data.get("email", ""),
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role="student",
            phone=self.cleaned_data.get("guardian_phone", ""),
            date_of_birth=self.cleaned_data.get("date_of_birth"),
            gender=self.cleaned_data.get("gender", ""),
            blood_group=self.cleaned_data.get("blood_group", ""),
            religion=self.cleaned_data.get("religion", ""),
        )

        if self.cleaned_data.get("profile_picture"):
            user.profile_picture = self.cleaned_data["profile_picture"]
            user.save()

        student = super().save(commit=False)
        student.user = user
        student.student_id = student_id

        if commit:
            student.save()

        return student
