from rest_framework import serializers, viewsets
from .models import Announcement, Message, Notification, Contact


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )

    class Meta:
        model = Announcement
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.get_full_name", read_only=True)
    recipient_name = serializers.CharField(
        source="recipient.get_full_name", read_only=True
    )

    class Meta:
        model = Message
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(
        source="recipient.get_full_name", read_only=True
    )

    class Meta:
        model = Notification
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    replied_by_name = serializers.CharField(
        source="replied_by.get_full_name", read_only=True
    )

    class Meta:
        model = Contact
        fields = "__all__"


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return Announcement.objects.all()
        return Announcement.objects.filter(
            Q(target_roles__contains=[user.role]) | Q(target_roles=[])
        ).filter(is_active=True)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        )


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
