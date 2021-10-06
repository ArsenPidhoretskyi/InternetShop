from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.views import WithContextView, SuperuserRequiredMixin
from .services import GetProducts, FilterParams, get_product
from .forms import ProductForm


class ProductsView(WithContextView):
    template_name = "product/Products.html"

    def get(self, request, *args, **kwargs):
        filter_params = FilterParams(request.GET)
        self.context = GetProducts(filter_params).get_context()
        return render(request, self.template_name, self.context)


class ProductCreateView(SuperuserRequiredMixin, WithContextView):
    template_name = "product/CreateProduct.html"
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect(reverse("product", args=(entry.id,)))
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class ProductView(WithContextView):
    template_name = "product/Product.html"

    def get(self, request, identifier: int, *args, **kwargs):
        self.context["product"] = get_product(identifier)
        return render(request, "product/Product.html", self.context)


class AddToCart(WithContextView):
    def post(self, request, identifier: int):
        add_product_to_cart(request.user, identifier)
