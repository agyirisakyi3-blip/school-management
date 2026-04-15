from django.db import models
from django.conf import settings


class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Book Category"
        verbose_name_plural = "Book Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(
        BookCategory, on_delete=models.SET_NULL, null=True, related_name="books"
    )
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.CharField(max_length=50, blank=True, help_text="Shelf location")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_available(self):
        return self.available_quantity > 0


class LibraryMember(models.Model):
    class MemberType(models.TextChoices):
        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"
        STAFF = "staff", "Staff"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="library_membership",
    )
    member_id = models.CharField(max_length=20, unique=True)
    member_type = models.CharField(max_length=20, choices=MemberType.choices)
    join_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    max_books = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Library Member"
        verbose_name_plural = "Library Members"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.member_id} - {self.user.get_full_name()}"

    @property
    def current_issues(self):
        return self.book_issues.filter(status="issued").count()

    @property
    def can_issue(self):
        return self.current_issues < self.max_books


class BookIssue(models.Model):
    class Status(models.TextChoices):
        ISSUED = "issued", "Issued"
        RETURNED = "returned", "Returned"
        OVERDUE = "overdue", "Overdue"
        LOST = "lost", "Lost"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_issues")
    member = models.ForeignKey(
        LibraryMember, on_delete=models.CASCADE, related_name="book_issues"
    )
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ISSUED
    )
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="issued_books",
    )

    class Meta:
        verbose_name = "Book Issue"
        verbose_name_plural = "Book Issues"
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.book.title} - {self.member.member_id}"

    @property
    def is_overdue(self):
        from datetime import date

        return self.status == self.Status.ISSUED and self.due_date < date.today()
