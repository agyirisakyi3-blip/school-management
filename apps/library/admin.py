from django.contrib import admin
from .models import Book, BookCategory, LibraryMember, BookIssue


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at"]
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "isbn",
        "author",
        "category",
        "quantity",
        "available_quantity",
    ]
    list_filter = ["category"]
    search_fields = ["title", "isbn", "author"]


@admin.register(LibraryMember)
class LibraryMemberAdmin(admin.ModelAdmin):
    list_display = ["member_id", "user", "member_type", "is_active", "join_date"]
    list_filter = ["member_type", "is_active"]
    search_fields = ["member_id", "user__first_name", "user__last_name"]


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ["book", "member", "issue_date", "due_date", "status", "fine_amount"]
    list_filter = ["status"]
    search_fields = ["book__title", "member__member_id"]
