from pathlib import Path
from typing import List

import django_stubs_ext
import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

django_stubs_ext.monkeypatch()


SECRET_KEY = env.str("DJANGO_SECRET_KEY")


DEBUG = True

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

ALLOWED_HOSTS: List[str] = []

INTERNAL_IPS = ["127.0.0.1"]

AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = env.str("EMAIL_HOST")
# EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
# EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
# EMAIL_PORT = env.int("EMAIL_PORT")
# EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

LOGIN_REDIRECT_URL = "books"
LOGOUT_REDIRECT_URL = "books"
LOGIN_URL = "login"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "debug_toolbar",
    "crispy_forms",
    "crispy_bootstrap5",
    "users.apps.UsersConfig",
    "books.apps.BooksConfig",
    "django_cleanup.apps.CleanupConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": "5432",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True
LANGUAGES = [("ru", _("Russian")), ("en", _("English"))]
LOCALE_PATHS = [str(BASE_DIR / "locale")]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_URL = "static/"
STATICFILES_DIRS = [str(BASE_DIR / "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
