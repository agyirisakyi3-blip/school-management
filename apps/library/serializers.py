from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book, BookCategory, LibraryMember, BookIssue


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "author",
            "publisher",
            "category",
            "category_name",
            "quantity",
            "available_quantity",
            "price",
            "location",
            "description",
            "is_available",
        ]


class LibraryMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = LibraryMember
        fields = [
            "id",
            "member_id",
            "user",
            "user_name",
            "member_type",
            "join_date",
            "expiry_date",
            "max_books",
            "is_active",
            "current_issues",
            "can_issue",
        ]


class BookIssueSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    member_name = serializers.CharField(
        source="member.user.get_full_name", read_only=True
    )
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = BookIssue
        fields = [
            "id",
            "book",
            "book_title",
            "member",
            "member_name",
            "issue_date",
            "due_date",
            "return_date",
            "status",
            "fine_amount",
            "notes",
            "is_overdue",
        ]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("category").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "author", "isbn"]
    filterset_fields = ["category", "is_available"]


class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes = [IsAuthenticated]


class LibraryMemberViewSet(viewsets.ModelViewSet):
    queryset = LibraryMember.objects.select_related("user").all()
    serializer_class = LibraryMemberSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["member_id", "user__first_name", "user__last_name"]
    filterset_fields = ["member_type", "is_active"]


class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.select_related("book", "member", "member__user").all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["book__title", "member__member_id"]
    filterset_fields = ["status", "is_overdue"]
