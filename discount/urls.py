from django.urls import path
from . import views

urlpatterns = [
    path("Discounts", views.DiscountsView.as_view(), name="discounts"),
    path("Discounts/<int:identifier>", views.DiscountView.as_view(), name="discount"),
    path("CreateDiscount", views.DiscountCreateView.as_view(), name="new_discount"),
    path(
        "ChangeDiscountStatus",
        views.DiscountStatusView.as_view(),
        name="change_discount_status",
    ),
]
