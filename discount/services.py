from .models import Discount
from django.core.exceptions import ObjectDoesNotExist


def get_discounts(user):
    if user.is_superuser:
        return Discount.objects.all()
    return Discount.objects.filter(activated=True)


def get_discount(identifier: int):
    try:
        product = Discount.objects.get(id=identifier)
        return product
    except ObjectDoesNotExist:
        return None


def change_status(identifier: int, status: bool):
    discount = get_discount(identifier)
    discount.activated = status
    discount.save()
