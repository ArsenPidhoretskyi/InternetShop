from django.urls import path
from . import views

urlpatterns = [
    path("Products", views.products_get, name="products_get"),
    path("Products/<int:identifier>", views.product_get, name="product_get"),
]
