from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, NonTeachingStaff


class UserCreationForm(UserCreationForm):
    """Form for creating new users."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "role", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["email"].required = True


class NonTeachingStaffCreationForm(forms.ModelForm):
    """Form for creating non-teaching staff with user account."""

    first_name = forms.CharField(max_length=150, label="First Name")
    last_name = forms.CharField(max_length=150, label="Last Name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    date_of_birth = forms.DateField(
        label="Date of Birth",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    gender = forms.ChoiceField(
        label="Gender", choices=User.Gender.choices, required=False
    )
    role = forms.ChoiceField(
        label="Staff Type",
        choices=[
            ("accountant", "Accountant"),
            ("librarian", "Librarian"),
            ("receptionist", "Receptionist"),
            ("driver", "Driver"),
            ("cook", "Cook"),
            ("guard", "Security Guard"),
            ("cleaner", "Cleaner"),
            ("maintenance", "Maintenance"),
            ("counselor", "Counselor"),
            ("nurse", "School Nurse"),
        ],
    )

    class Meta:
        model = NonTeachingStaff
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "department",
            "designation",
            "employment_date",
            "salary",
            "contract_type",
            "shift_timing",
            "emergency_contact_name",
            "emergency_contact_phone",
            "qualifications",
            "experience_years",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget = self.fields[field].widget
            if isinstance(widget, forms.Select):
                widget.attrs.update({"class": "form-select"})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": "form-check-input"})
            elif not isinstance(widget, (forms.DateInput, forms.PasswordInput)):
                widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        username_base = (
            self.cleaned_data.get("email", "").split("@")[0]
            if self.cleaned_data.get("email")
            else "staff"
        )
        username = f"{username_base}{NonTeachingStaff.objects.count() + 1}"

        user = User.objects.create_user(
            username=username,
            email=self.cleaned_data.get("email", ""),
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role=self.cleaned_data["role"],
            phone=self.cleaned_data.get("emergency_contact_phone", ""),
            date_of_birth=self.cleaned_data.get("date_of_birth"),
            gender=self.cleaned_data.get("gender", ""),
        )

        staff = super().save(commit=False)
        staff.user = user
        if commit:
            staff.save()
        return staff


class NonTeachingStaffForm(forms.ModelForm):
    """Form for updating non-teaching staff."""

    class Meta:
        model = NonTeachingStaff
        fields = [
            "department",
            "designation",
            "employment_date",
            "salary",
            "contract_type",
            "shift_timing",
            "emergency_contact_name",
            "emergency_contact_phone",
            "qualifications",
            "experience_years",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget = self.fields[field].widget
            if isinstance(widget, forms.Select):
                widget.attrs.update({"class": "form-select"})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": "form-check-input"})
            elif not isinstance(widget, (forms.DateInput,)):
                widget.attrs.update({"class": "form-control"})


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information."""

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "address",
            "profile_picture",
        ]


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""

    class Meta:
        model = UserProfile
        fields = ["bio", "emergency_contact", "blood_group", "religion", "nationality"]


class UserAdminForm(forms.ModelForm):
    """Form for admin user management."""

    class Meta:
        model = User
        fields = "__all__"


class AdminUserCreateForm(UserCreationForm):
    """Enhanced form for admins creating any user type."""

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "gender",
            "date_of_birth",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["role"].widget.attrs.update({"class": "form-select"})
        self.fields["gender"].widget.attrs.update({"class": "form-select"})
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class AdminUserEditForm(forms.ModelForm):
    """Form for admins editing any user."""

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "gender",
            "date_of_birth",
            "address",
            "is_active",
            "profile_picture",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget = self.fields[field].widget
            if isinstance(widget, forms.Select):
                widget.attrs.update({"class": "form-select"})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": "form-check-input"})
            elif not isinstance(widget, forms.FileInput):
                widget.attrs.update({"class": "form-control"})


class AdminPasswordChangeForm(forms.Form):
    """Form for admins to reset a user's password."""

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password1")
        p2 = cleaned_data.get("new_password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserProfileUpdateForm(forms.ModelForm):
    """Form for students/teachers/parents to update their own profile picture."""

    class Meta:
        model = User
        fields = ["profile_picture"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_picture"].widget.attrs.update({"class": "form-control"})
