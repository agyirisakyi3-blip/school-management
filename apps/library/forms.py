from django import forms
from .models import Book, BookCategory, LibraryMember, BookIssue


class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "isbn",
            "author",
            "publisher",
            "category",
            "quantity",
            "price",
            "location",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "publisher": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ["book", "member", "due_date", "notes"]
        widgets = {
            "book": forms.Select(attrs={"class": "form-select"}),
            "member": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(available_quantity__gt=0)


class BookReturnForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ["return_date", "fine_amount", "notes"]
        widgets = {
            "return_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "fine_amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = ["user", "member_type", "max_books", "expiry_date"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "member_type": forms.Select(attrs={"class": "form-select"}),
            "max_books": forms.NumberInput(attrs={"class": "form-control"}),
            "expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
