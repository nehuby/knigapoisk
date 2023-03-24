from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("books/", views.books, name="books"),
    path("book/<int:pk>/", views.book, name="book"),
    path("book/create/", views.book_create, name="book_create"),
    path("book/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("book/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("mybooks/", views.my_books, name="my_books"),
    path("authors/", views.authors, name="authors"),
    path("author/<int:pk>/", views.author, name="author"),
    path("author/create/", views.author_create, name="author_create"),
    path("genres/", views.genres, name="genres"),
    path("genre/<int:pk>/", views.genre, name="genre"),
    path("genre/create/", views.genre_create, name="genre_create"),
    path("translator/create/", views.translator_create, name="translator_create"),
    path("reveiw/<int:pk>/edit/", views.review_edit, name="review_edit"),
    path("reveiw/<int:pk>/delete/", views.review_delete, name="review_delete"),
]
