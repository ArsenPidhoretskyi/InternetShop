from django.shortcuts import render
from . import services


def products_get(request):
    context = dict()
    if request.method == "GET":
        context["products"] = services.get_products()
        return render(request, "product/Products.html", context)


def product_get(request, identifier: int):
    context = dict()
    if request.method == "GET":
        context["product"] = services.get_product(identifier)
        return render(request, "product/Product.html", context)


def product_create(request):
    if request.method == "GET":
        return render(request, "product/CreateProduct.html")
    if request.method == "POST":
        product = services.create_product(request.POST)
        return
