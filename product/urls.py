from django.urls import path
from . import views

urlpatterns = [
    path(r"Products", views.ProductsView.as_view(), name="products"),
    path(r"SearchProducts", views.SearchProducts.as_view(), name="search_products"),
    path(r"Products/<int:identifier>", views.ProductView.as_view(), name="product"),
    path(r"NewProduct", views.ProductCreateView.as_view(), name="new_product"),
    path(
        r"UpdateProduct/<int:identifier>",
        views.UpdateProduct.as_view(),
        name="update_product",
    ),
    path(r"AddToCart", views.AddToCartView.as_view(), name="add_to_cart"),
    path(
        r"RemoveFromCart", views.RemoveFromCartView.as_view(), name="remove_from_cart"
    ),
    path(
        r"DeleteFromCart", views.DeleteFromCartView.as_view(), name="delete_from_cart"
    ),
    path(r"Cart", views.CartView.as_view(), name="cart"),
]
