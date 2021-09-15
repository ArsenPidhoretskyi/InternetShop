from django.core.exceptions import ObjectDoesNotExist

from .models import Product


def get_products():
    return Product.objects.all()


def get_product(identifier: int):
    try:
        product = Product.objects.get(id=identifier)
        return product
    except ObjectDoesNotExist:
        return None


def create_product(properties):
    pass
