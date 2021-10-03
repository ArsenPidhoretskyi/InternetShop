from django.urls import path, include

from . import views


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("profile", views.ProfileView.as_view(), name="me"),
]
