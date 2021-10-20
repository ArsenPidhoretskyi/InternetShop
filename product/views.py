from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from core.views import WithContextView, SuperuserRequiredMixin, View
from .services import *
from .forms import ProductForm


class ProductsView(WithContextView):
    template_name = "product/Products.html"

    def get(self, *args, **kwargs):
        filter_params = FilterParams(self.request.GET)
        self.context = GetProducts(filter_params).get_context()
        return render(self.request, self.template_name, self.context)


class ProductCreateView(SuperuserRequiredMixin, WithContextView):
    template_name = "product/CreateProduct.html"
    form_class = ProductForm

    def get(self, *args, **kwargs):
        self.context["form"] = self.form_class()
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect(reverse("product", args=(entry.id,)))
        self.context["form"] = form
        return render(self.request, self.template_name, self.context)


class ProductView(WithContextView):
    template_name = "product/Product.html"

    def get(self, *args, identifier: int, **kwargs):
        self.context["product"] = get_product(identifier)
        return render(self.request, self.template_name, self.context)

    @staticmethod
    def delete(*args, identifier: int, **kwargs):
        get_product(identifier).delete()
        return JsonResponse({"url": reverse("products")})


class SearchProducts(View):
    def get(self, *args, **kwargs):
        search = self.request.GET.get("search", "")
        products = GetProducts.search_products(search)
        return JsonResponse(
            {"products": list(map(lambda product: product.as_dict(), products))}
        )


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
