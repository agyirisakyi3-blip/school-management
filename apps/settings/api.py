from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    SchoolInfo,
    GeneralSettings,
    EmailSettings,
    ThemeSettings,
    AttendanceSettings,
    ResultSettings,
    FeeSettings,
)
from .serializers import (
    SchoolInfoSerializer,
    GeneralSettingsSerializer,
    EmailSettingsSerializer,
    ThemeSettingsSerializer,
    AttendanceSettingsSerializer,
    ResultSettingsSerializer,
    FeeSettingsSerializer,
)


class IsAdminUser:
    def has_permission(self, request, view):
        return request.user and request.user.is_admin_user


class SchoolInfoViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolInfoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return SchoolInfo.get_instance()

    def list(self, request):
        instance = SchoolInfo.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = SchoolInfo.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GeneralSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = GeneralSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return GeneralSettings.get_instance()

    def list(self, request):
        instance = GeneralSettings.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = GeneralSettings.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EmailSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = EmailSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return EmailSettings.get_instance()

    def list(self, request):
        instance = EmailSettings.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = EmailSettings.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ThemeSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = ThemeSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return ThemeSettings.get_instance()

    def list(self, request):
        instance = ThemeSettings.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = ThemeSettings.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AttendanceSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return AttendanceSettings.get_instance()

    def list(self, request):
        instance = AttendanceSettings.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = AttendanceSettings.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResultSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return ResultSettings.get_instance()

    def list(self, request):
        instance = ResultSettings.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = ResultSettings.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FeeSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = FeeSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        return FeeSettings.get_instance()

    def list(self, request):
        instance = FeeSettings.get_instance()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = FeeSettings.get_instance()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
