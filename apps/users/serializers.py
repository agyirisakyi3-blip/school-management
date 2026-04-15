from rest_framework import serializers, viewsets, permissions
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "address",
            "profile_picture",
            "date_of_birth",
            "profile",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return User.objects.all()
        elif user.is_teacher:
            return User.objects.filter(role=User.Role.TEACHER) | User.objects.filter(
                role=User.Role.STUDENT
            )
        elif user.is_student:
            return User.objects.filter(id=user.id)
        elif user.is_parent:
            return User.objects.filter(id=user.id)
        return User.objects.filter(id=user.id)
