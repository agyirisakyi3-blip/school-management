from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/create/", views.BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/<int:pk>/update/", views.BookUpdateView.as_view(), name="book_update"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
    path("categories/", views.BookCategoryListView.as_view(), name="category_list"),
    path(
        "categories/create/",
        views.BookCategoryCreateView.as_view(),
        name="category_create",
    ),
    path(
        "categories/<int:pk>/update/",
        views.BookCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.BookCategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path("members/", views.LibraryMemberListView.as_view(), name="member_list"),
    path(
        "members/create/", views.LibraryMemberCreateView.as_view(), name="member_create"
    ),
    path("issues/", views.BookIssueListView.as_view(), name="issue_list"),
    path("issues/create/", views.BookIssueCreateView.as_view(), name="issue_create"),
    path("issues/<int:pk>/return/", views.BookReturnView.as_view(), name="book_return"),
]
