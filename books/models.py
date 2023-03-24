from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import languages, validators


class Genre(models.Model):
    name = models.CharField(_("name"), unique=True, max_length=100)

    class Meta:
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    name = models.CharField(_("name"), unique=True, max_length=100)
    about = models.TextField(_("about"), blank=True)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self) -> str:
        return self.name


class Translator(models.Model):
    name = models.CharField(_("name"), unique=True, max_length=100)

    class Meta:
        verbose_name = _("translator")
        verbose_name_plural = _("translators")

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    number_of_pages = models.PositiveIntegerField(_("number of pages"))
    year_of_publication = models.PositiveSmallIntegerField(
        _("year of publication"), validators=[validators.validator]
    )
    language = models.CharField(_("language"), max_length=50, choices=languages.choices)
    photo = models.ImageField(_("photo"), upload_to="books/")
    genres = models.ManyToManyField(
        Genre, verbose_name=_("genres"), related_name="books"
    )
    authors = models.ManyToManyField(
        Author, verbose_name=_("authors"), related_name="books"
    )
    translators = models.ManyToManyField(
        Translator, verbose_name=_("translators"), related_name="books", blank=True
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("creator"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")

    def __str__(self) -> str:
        return self.name


class BookReview(models.Model):
    RATING = tuple((i, str(i)) for i in range(1, 11))
    name = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("name"), on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book, verbose_name=_("book"), on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField(_("text"))
    date = models.DateTimeField(_("date"), auto_now=True)
    score = models.PositiveSmallIntegerField(_("score"), choices=RATING)

    def __str__(self) -> str:
        return self.text
