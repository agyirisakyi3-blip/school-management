from django import forms
from .models import Announcement, Message, Notification, Contact


class AnnouncementForm(forms.ModelForm):
    """Form for Announcement."""

    target_roles = forms.MultipleChoiceField(
        choices=[
            ("admin", "Admin"),
            ("teacher", "Teacher"),
            ("student", "Student"),
            ("parent", "Parent"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Target Roles",
    )

    class Meta:
        model = Announcement
        fields = [
            "title",
            "content",
            "priority",
            "target_roles",
            "target_classes",
            "is_active",
            "expiry_date",
        ]
        widgets = {
            "expiry_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["target_roles", "target_classes"]:
                self.fields[field].widget.attrs.update({"class": "form-control"})
        if self.instance and self.instance.target_roles:
            self.initial["target_roles"] = self.instance.get_target_roles_list()

    def clean_target_roles(self):
        roles = self.cleaned_data.get("target_roles", [])
        if not roles:
            return "all"
        return ",".join(roles)


class MessageForm(forms.ModelForm):
    """Form for Message."""

    class Meta:
        model = Message
        fields = ["recipient", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class MessageReplyForm(forms.ModelForm):
    """Form for replying to a message."""

    class Meta:
        model = Message
        fields = ["body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ContactForm(forms.ModelForm):
    """Form for Contact."""

    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "subject", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
