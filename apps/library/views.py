from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from datetime import date, timedelta
from .models import Book, BookCategory, LibraryMember, BookIssue
from .forms import (
    BookForm,
    BookCategoryForm,
    BookIssueForm,
    BookReturnForm,
    LibraryMemberForm,
)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin_user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("users:dashboard")


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "library/book_list.html"
    context_object_name = "books"
    paginate_by = 20

    def get_queryset(self):
        queryset = Book.objects.select_related("category")
        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        availability = self.request.GET.get("availability")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(author__icontains=search)
                | Q(isbn__icontains=search)
            )
        if category:
            queryset = queryset.filter(category_id=category)
        if availability == "available":
            queryset = queryset.filter(available_quantity__gt=0)
        elif availability == "unavailable":
            queryset = queryset.filter(available_quantity=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = BookCategory.objects.all()
        context["total_books"] = Book.objects.count()
        context["available_books"] = Book.objects.filter(
            available_quantity__gt=0
        ).count()
        context["total_copies"] = (
            Book.objects.aggregate(total=Sum("quantity"))["total"] or 0
        )
        context["search"] = self.request.GET.get("search", "")
        context["category_filter"] = self.request.GET.get("category", "")
        context["availability_filter"] = self.request.GET.get("availability", "")
        return context


from django.db.models import Sum


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"


class BookCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:book_list")

    def form_valid(self, form):
        messages.success(self.request, "Book added successfully.")
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:book_list")

    def form_valid(self, form):
        messages.success(self.request, "Book updated successfully.")
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Book
    template_name = "library/book_confirm_delete.html"
    success_url = reverse_lazy("library:book_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Book deleted successfully.")
        return super().delete(request, *args, **kwargs)


class BookCategoryListView(LoginRequiredMixin, ListView):
    model = BookCategory
    template_name = "library/category_list.html"
    context_object_name = "categories"


class BookCategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = BookCategory
    form_class = BookCategoryForm
    template_name = "library/category_form.html"
    success_url = reverse_lazy("library:category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)


class BookCategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = BookCategory
    form_class = BookCategoryForm
    template_name = "library/category_form.html"
    success_url = reverse_lazy("library:category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)


class BookCategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = BookCategory
    template_name = "library/category_confirm_delete.html"
    success_url = reverse_lazy("library:category_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Category deleted successfully.")
        return super().delete(request, *args, **kwargs)


class LibraryMemberListView(LoginRequiredMixin, ListView):
    model = LibraryMember
    template_name = "library/member_list.html"
    context_object_name = "members"
    paginate_by = 20

    def get_queryset(self):
        queryset = LibraryMember.objects.select_related("user")
        search = self.request.GET.get("search")
        member_type = self.request.GET.get("type")

        if search:
            queryset = queryset.filter(
                Q(member_id__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
            )
        if member_type:
            queryset = queryset.filter(member_type=member_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_members"] = LibraryMember.objects.count()
        context["active_members"] = LibraryMember.objects.filter(is_active=True).count()
        return context


class LibraryMemberCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = LibraryMember
    form_class = LibraryMemberForm
    template_name = "library/member_form.html"
    success_url = reverse_lazy("library:member_list")

    def form_valid(self, form):
        messages.success(self.request, "Member added successfully.")
        return super().form_valid(form)


class BookIssueListView(LoginRequiredMixin, ListView):
    model = BookIssue
    template_name = "library/issue_list.html"
    context_object_name = "issues"
    paginate_by = 20

    def get_queryset(self):
        queryset = BookIssue.objects.select_related("book", "member", "member__user")
        status = self.request.GET.get("status")
        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                Q(book__title__icontains=search)
                | Q(member__user__first_name__icontains=search)
                | Q(member__member_id__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        elif not status:
            queryset = queryset.filter(status="issued")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issued_count"] = BookIssue.objects.filter(status="issued").count()
        context["overdue_count"] = BookIssue.objects.filter(
            status="issued", due_date__lt=date.today()
        ).count()
        context["returned_count"] = BookIssue.objects.filter(status="returned").count()
        context["status_filter"] = self.request.GET.get("status", "issued")
        return context


class BookIssueCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = BookIssue
    form_class = BookIssueForm
    template_name = "library/issue_form.html"
    success_url = reverse_lazy("library:issue_list")

    def form_valid(self, form):
        form.instance.issued_by = self.request.user
        book = form.cleaned_data["book"]
        book.available_quantity = max(0, book.available_quantity - 1)
        book.save()
        messages.success(self.request, "Book issued successfully.")
        return super().form_valid(form)


class BookReturnView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        issue = get_object_or_404(BookIssue, pk=pk)
        form = BookReturnForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.status = BookIssue.Status.RETURNED
            issue.book.available_quantity += 1
            issue.book.save()
            issue.save()
            messages.success(request, "Book returned successfully.")
        return redirect("library:issue_list")
