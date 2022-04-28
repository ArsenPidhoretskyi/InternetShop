from django.urls import path, include

from . import views


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("Signup", views.SignUpView.as_view(), name="signup"),
    path("Profile", views.ProfileView.as_view(), name="me"),
]
