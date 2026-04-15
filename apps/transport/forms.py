from django import forms
from .models import TransportRoute, Vehicle, VehicleRoute, StudentTransport


class TransportRouteForm(forms.ModelForm):
    class Meta:
        model = TransportRoute
        fields = ["name", "route_from", "route_to", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "route_from": forms.TextInput(attrs={"class": "form-control"}),
            "route_to": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "vehicle_number",
            "vehicle_type",
            "model",
            "capacity",
            "driver_name",
            "driver_phone",
            "license_number",
            "is_active",
        ]
        widgets = {
            "vehicle_number": forms.TextInput(attrs={"class": "form-control"}),
            "vehicle_type": forms.Select(attrs={"class": "form-select"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "driver_name": forms.TextInput(attrs={"class": "form-control"}),
            "driver_phone": forms.TextInput(attrs={"class": "form-control"}),
            "license_number": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class VehicleRouteForm(forms.ModelForm):
    class Meta:
        model = VehicleRoute
        fields = [
            "route",
            "vehicle",
            "driver",
            "pickup_time",
            "drop_time",
            "fare",
            "is_active",
        ]
        widgets = {
            "route": forms.Select(attrs={"class": "form-select"}),
            "vehicle": forms.Select(attrs={"class": "form-select"}),
            "driver": forms.Select(attrs={"class": "form-select"}),
            "pickup_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "drop_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "fare": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class StudentTransportForm(forms.ModelForm):
    class Meta:
        model = StudentTransport
        fields = ["student", "vehicle_route", "pickup_point", "is_active"]
        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "vehicle_route": forms.Select(attrs={"class": "form-select"}),
            "pickup_point": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
