from django.urls import path
from . import views

urlpatterns = [
    path(r"Purchase", views.CreatePurchaseView.as_view(), name="create_purchase"),
    path(r"History", views.PurchasesView.as_view(), name="history"),
]
