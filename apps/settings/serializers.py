from rest_framework import serializers
from .models import (
    SchoolInfo,
    GeneralSettings,
    EmailSettings,
    ThemeSettings,
    AttendanceSettings,
    ResultSettings,
    FeeSettings,
)


class SchoolInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolInfo
        fields = "__all__"


class GeneralSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSettings
        fields = "__all__"


class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSettings
        fields = "__all__"
        extra_kwargs = {"email_host_password": {"write_only": True}}


class ThemeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSettings
        fields = "__all__"


class AttendanceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSettings
        fields = "__all__"


class ResultSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultSettings
        fields = "__all__"


class FeeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeSettings
        fields = "__all__"
