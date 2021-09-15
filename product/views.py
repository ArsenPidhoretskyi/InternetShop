from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from . import services
from .forms import ProductForm


class WithContextView(View):
    def __init__(self, **kwargs):
        super(WithContextView, self).__init__(**kwargs)
        self.context = dict()


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
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("product:new_product"))
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class ProductView(WithContextView):
    template_name = "product/Product.html"

    def get(self, request, identifier: int, *args, **kwargs):
        self.context["product"] = services.get_product(identifier)
        return render(request, "product/Product.html", self.context)
