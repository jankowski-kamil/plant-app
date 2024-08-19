from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView
from rest_framework_simplejwt.views import TokenRefreshView
from django_rest_passwordreset.views import ResetPasswordRequestToken

from .views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    CustomResetPasswordConfirmView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path(
        "password/confirm-reset/",
        CustomResetPasswordConfirmView.as_view(),
        name="password_change_confirm",
    ),
    path("password/reset/", ResetPasswordRequestToken.as_view(), name="password_reset"),
]
