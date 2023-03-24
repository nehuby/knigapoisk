from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, TemplateView

from .forms import Signup, token_generator
from .models import User


class SignUpView(CreateView):
    form_class = Signup
    template_name = "registration/signup.html"
    success_url = reverse_lazy("check_email")

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = form.save()
        user.is_active = False
        user.save()

        form.send_activation_email(self.request, user)

        return to_return


class ActivateView(RedirectView):

    url = reverse_lazy("success")

    def get(self, request: HttpRequest, uidb64, token) -> HttpResponse:

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, "registration/activate_account_invalid.html")


class CheckEmailView(TemplateView):
    template_name = "registration/check_email.html"


class SuccessView(TemplateView):
    template_name = "registration/success.html"
