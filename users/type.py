from django.contrib.auth.models import User
from django.http import HttpRequest


class Request(HttpRequest):
    user: User
