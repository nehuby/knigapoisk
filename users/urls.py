from django.contrib.auth import views as auth_views
from django.urls import path

from .views import ActivateView, CheckEmailView, SignUpView, SuccessView

urlpatterns = [
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("check-email/", CheckEmailView.as_view(), name="check_email"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset_form",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "set-password/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("success/", SuccessView.as_view(), name="success"),
]
