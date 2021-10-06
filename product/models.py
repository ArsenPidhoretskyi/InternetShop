from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime

User = get_user_model()


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.IntegerField()
    available = models.IntegerField()
    image = models.ImageField(upload_to="products")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product"

    def __repr__(self):
        return f"Product<id={self.id}>"


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "User: {} has {} items in their cart. Their total is ${}".format(
            self.user, self.count, self.total
        )


class Entry(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, null=True, on_delete="CASCADE")
    cart = models.ForeignKey(Cart, null=True, on_delete="CASCADE")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.product.name)


@receiver(post_save, sender=Entry)
def update_cart(sender, instance, **kwargs):
    line_cost = instance.quantity * instance.product.price
    instance.cart.total += line_cost
    instance.cart.count += instance.quantity
    instance.cart.updated = datetime.now()
