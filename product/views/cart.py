from django.http import JsonResponse
from django.shortcuts import render

from core.views import WithContextView, View
from product.services import *


class CartView(WithContextView):
    template_name = "cart/Cart.html"

    def get(self, *args, **kwargs):
        self.context = get_cart_entries(self.request.user)
        return render(self.request, self.template_name, self.context)


class AddToCartView(View):
    def post(self, *args, **kwargs):
        product_id = self.request.POST["id"]
        cart, product = add_product_to_cart(self.request.user, product_id)
        response = {"new_total": cart.total, "new_product_total": product.total}
        return JsonResponse(response)


class RemoveFromCartView(View):
    def post(self, *args, **kwargs):
        product_id = self.request.POST["id"]
        cart, product = remove_product_from_cart(self.request.user, product_id)
        response = {"new_total": cart.total, "new_product_total": product.total}
        return JsonResponse(response)


class DeleteFromCartView(View):
    def post(self, *args, **kwargs):
        product_id = self.request.POST["id"]
        cart = delete_product_from_cart(self.request.user, product_id)
        response = {"new_total": cart.total}
        return JsonResponse(response)
