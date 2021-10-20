from product.models import Cart
from .models import Purchase, Order


def create_order(user):
    cart = Cart.objects.get(user=user)
    if not cart.entry_set.all():
        return
    order = Order.objects.create(user=user)
    total = 0
    for entry in cart.entry_set.all():
        Purchase.objects.create(
            quantity=entry.quantity,
            product=entry.product,
            total=entry.total,
            order=order,
        )
        total += entry.total
    order.total = total
    order.save()
    cart.delete()


def get_orders(user):
    return Order.objects.filter(user=user)
