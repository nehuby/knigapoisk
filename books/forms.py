from typing import Any

from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Author, Book, BookReview, Genre, Translator


class BookForm(ModelForm[Book]):
    class Meta:
        model = Book
        fields = [
            "name",
            "description",
            "authors",
            "genres",
            "year_of_publication",
            "number_of_pages",
            "language",
            "translators",
            "photo",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "genres": forms.CheckboxSelectMultiple,
            "authors": forms.CheckboxSelectMultiple(),
            "translators": forms.CheckboxSelectMultiple,
        }
        labels = {
            "authors": "",
            "genres": "",
            "translators": "",
        }


class BookReviewForm(ModelForm[BookReview]):
    class Meta:
        model = BookReview
        fields = ["score", "text"]
        widgets = {"text": forms.Textarea({"rows": 3})}


class AuthorForm(ModelForm[Author]):
    class Meta:
        model = Author
        fields = ["name", "about"]
        widgets = {"about": forms.Textarea({"rows": 3})}


class GenreForm(ModelForm[Genre]):
    class Meta:
        model = Genre
        fields = ["name"]


class TranslatorForm(ModelForm[Translator]):
    class Meta:
        model = Translator
        fields = ["name"]


class PostSearchForm(forms.Form):
    q = forms.Field(
        widget=forms.TextInput({"class": "form-control", "placeholder": _("Search")}),
        label=_("Search"),
    )
