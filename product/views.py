from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.views import WithContextView
from . import services
from .forms import ProductForm


class ProductsView(WithContextView):
    template_name = "product/Products.html"

    def get(self, request, *args, **kwargs):
        self.context["products"] = services.get_products()
        return render(request, self.template_name, self.context)


class ProductCreateView(WithContextView):
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
        self.context["product"] = services.get_product(identifier)
        return render(request, "product/Product.html", self.context)
