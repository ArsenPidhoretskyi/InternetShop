from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from core.views import WithContextView, SuperuserRequiredMixin, View
from product.services import *
from product.forms import ProductForm

from django.urls import reverse


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
    form_class = ProductForm

    def get(self, *args, identifier: int, **kwargs):
        self.context["product"] = get_product(identifier)
        return render(self.request, self.template_name, self.context)


class UpdateProduct(WithContextView):
    template_name = "product/CreateProduct.html"
    form_class = ProductForm

    def get(self, *args, identifier: int, **kwargs):
        self.context["form"] = self.form_class(instance=get_product(identifier))
        return render(self.request, self.template_name, self.context)

    def post(self, *args, identifier: int, **kwargs):
        self.context["product"] = get_product(identifier)
        form = self.form_class(
            self.request.POST, self.request.FILES, instance=self.context["product"]
        )
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect(reverse("product", args=(entry.id,)))
        self.context["form"] = form
        return render(self.request, "product/CreateProduct.html", self.context)

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
