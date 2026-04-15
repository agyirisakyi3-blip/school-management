from django import forms
from .models import Dormitory, Room, StudentRoom


class DormitoryForm(forms.ModelForm):
    class Meta:
        model = Dormitory
        fields = [
            "name",
            "type",
            "address",
            "warden_name",
            "warden_phone",
            "total_rooms",
            "capacity",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "warden_name": forms.TextInput(attrs={"class": "form-control"}),
            "warden_phone": forms.TextInput(attrs={"class": "form-control"}),
            "total_rooms": forms.NumberInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            "dormitory",
            "room_number",
            "room_type",
            "floor",
            "total_beds",
            "cost_per_bed",
            "is_available",
            "description",
        ]
        widgets = {
            "dormitory": forms.Select(attrs={"class": "form-select"}),
            "room_number": forms.TextInput(attrs={"class": "form-control"}),
            "room_type": forms.Select(attrs={"class": "form-select"}),
            "floor": forms.NumberInput(attrs={"class": "form-control"}),
            "total_beds": forms.NumberInput(attrs={"class": "form-control"}),
            "cost_per_bed": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class StudentRoomForm(forms.ModelForm):
    class Meta:
        model = StudentRoom
        fields = [
            "student",
            "room",
            "bed_number",
            "start_date",
            "end_date",
            "is_active",
        ]
        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "room": forms.Select(attrs={"class": "form-select"}),
            "bed_number": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
