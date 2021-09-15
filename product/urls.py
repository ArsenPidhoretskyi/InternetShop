from django.urls import path
from . import views

urlpatterns = [
    path(r"Products", views.ProductsView.as_view(), name="products"),
    path(r"Products/<int:identifier>", views.ProductView.as_view(), name="product"),
    path(r"NewProduct", views.ProductCreateView.as_view(), name="new_product"),
]
