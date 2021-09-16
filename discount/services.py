from .models import Discount
from django.core.exceptions import ObjectDoesNotExist


def get_discounts():
    return Discount.objects.all()


def get_discount(identifier):
    try:
        product = Discount.objects.get(id=identifier)
        return product
    except ObjectDoesNotExist:
        return None
