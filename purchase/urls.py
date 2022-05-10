from django.urls import path
from . import views

urlpatterns = [
    path(r"Order", views.CreateOrderView.as_view(), name="create_order"),
    path(r"History", views.PurchasesView.as_view(), name="history"),
]
