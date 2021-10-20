from product.models import Cart
from .models import Purchase


def create_purchase(user):
    cart = Cart.objects.get(user=user)
    for entry in cart.entry_set.all():
        Purchase.objects.create(
            quantity=entry.quantity, product=entry.product, user=user, total=entry.total
        )
    cart.delete()


def get_purchases(user):
    return Purchase.objects.filter(user=user)
