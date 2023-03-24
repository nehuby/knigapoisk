from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import Avg, Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from users.type import Request

from .forms import (
    AuthorForm,
    BookForm,
    BookReviewForm,
    GenreForm,
    PostSearchForm,
    TranslatorForm,
)
from .models import Author, Book, BookReview, Genre


def index(request: HttpRequest) -> HttpResponse:
    return redirect("books")


def books(request: HttpRequest) -> HttpResponse:
    books: QuerySet[Book]
    if "q" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            vector = SearchVector(
                "name", "authors__name", "genres__name", "translators__name"
            )
            books = (
                Book.objects.annotate(search=vector)
                .prefetch_related(
                    Prefetch("authors", queryset=Author.objects.only("name"))
                )
                .filter(search=form.cleaned_data["q"])
            )
    else:
        form = PostSearchForm()
        books = (
            Book.objects.prefetch_related(
                Prefetch("authors", queryset=Author.objects.only("name"))
            )
            .only("name")
            .order_by("name")
        )
    context = {"books": books, "form": form}
    return render(request, "books/books.html", context)


def book(request: HttpRequest, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    rate = BookReview.objects.filter(book=book).aggregate(avg_score=Avg("score"))
    paginator = Paginator(BookReview.objects.filter(book=book).order_by("-date"), 3)
    try:
        page_number = int(request.GET["page"])
    except (KeyError, ValueError):
        page_number = 1
    else:
        if page_number < 1:
            page_number = 1
        elif page_number > paginator.num_pages:
            page_number = paginator.num_pages
    reviews = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_number, on_each_side=1, on_ends=1
    )
    if request.method == "POST":
        if request.user.is_authenticated:
            form = BookReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.name = request.user
                review.book = book
                review.save()
                return redirect("book", pk=book.pk)
    else:
        form = BookReviewForm()
    context = {
        "book": book,
        "form": form,
        "rate": round(rate["avg_score"] or 0, 1),
        "reviews": reviews,
        "page_range": page_range,
    }
    return render(request, "books/book.html", context)


def authors(request: HttpRequest) -> HttpResponse:
    authors = Author.objects.all().order_by("name")
    context = {"authors": authors}
    return render(request, "books/authors.html", context)


def author(request: HttpRequest, pk: int) -> HttpResponse:
    author = get_object_or_404(Author, pk=pk)
    context = {"author": author}
    return render(request, "books/author.html", context)


def genres(request: HttpRequest) -> HttpResponse:
    genres = Genre.objects.all().order_by("name")
    context = {"genres": genres}
    return render(request, "books/genres.html", context)


def genre(request: HttpRequest, pk: int) -> HttpResponse:
    genre = get_object_or_404(Genre, pk=pk)
    context = {"genre": genre}
    return render(request, "books/genre.html", context)


@login_required
def my_books(request: Request) -> HttpResponse:
    books = (
        Book.objects.filter(creator=request.user)
        .order_by("name")
        .prefetch_related(Prefetch("authors", queryset=Author.objects.only("name")))
    )
    context = {"books": books}
    return render(request, "books/my_books.html", context)


@login_required
def book_edit(request: Request, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(instance=book)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("my_books")
    context = {"form": form}
    return render(request, "books/book_edit.html", context)


@login_required
def book_delete(request: Request, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("my_books")
    context = {"book": book}
    return render(request, "books/my_books.html", context)


@login_required
def review_delete(request: Request, pk: int) -> HttpResponse:
    reveiw = get_object_or_404(BookReview, pk=pk)
    if request.method == "POST":
        reveiw.delete()
        return redirect("book", reveiw.book_id)
    context = {"reveiw": reveiw}
    return render(request, "books/book.html", context)


@login_required
def review_edit(request: Request, pk: int) -> HttpResponse:
    review = get_object_or_404(BookReview, pk=pk)
    form = BookReviewForm(instance=review)
    if request.method == "POST":
        form = BookReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect("book", review.book_id)
    context = {"form": form}
    return render(request, "books/book.html", context)


@login_required
def book_create(request: Request) -> HttpResponse:
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.creator = request.user
            book.save()
            form.save_m2m()
            return redirect("my_books")
    context = {"form": form}
    return render(request, "books/book_create.html", context)


@login_required
def author_create(request: Request) -> HttpResponse:
    form = AuthorForm()
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            form.save()
            messages.success(request, _(f"Created new author - {name}"))
            form = AuthorForm()
    context = {"form": form}
    return render(request, "books/author_create.html", context)


@login_required
def genre_create(request: Request) -> HttpResponse:
    form = GenreForm()
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            form.save()
            messages.success(request, f"Created new genre - {name}")
            form = GenreForm()
    context = {"form": form}
    return render(request, "books/genre_create.html", context)


@login_required
def translator_create(request: Request) -> HttpResponse:
    form = TranslatorForm()
    if request.method == "POST":
        form = TranslatorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            form.save()
            messages.success(request, f"Created new translator - {name}")
            form = TranslatorForm()
    context = {"form": form}
    return render(request, "books/translator_create.html", context)
