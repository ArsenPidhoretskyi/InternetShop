from django.urls import path
from . import views

urlpatterns = [
    path(r"Purchase", views.CreatePurchase.as_view(), name="create_purchase"),
]
