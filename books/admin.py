from django.contrib import admin

from .models import Author, Book, BookReview, Genre, Translator


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin[Genre]):
    list_display = ("id", "name")
    list_display_links = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin[Author]):
    list_display = ("id", "name")
    list_display_links = ("name",)


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin[Translator]):
    list_display = ("id", "name")
    list_display_links = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin[Book]):
    list_display = ("id", "name", "language")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    filter_horizontal = ("genres", "authors", "translators")


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin[BookReview]):
    list_display = ("id", "name", "date")
    list_display_links = ("name",)
