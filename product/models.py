from django.contrib.auth import get_user_model
from django.db import models
from decimal import Decimal
from django.db.models import Max, Min

from django.utils.datetime_safe import datetime

User = get_user_model()


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    available = models.IntegerField()
    image = models.ImageField(upload_to="products")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product"
        ordering = ["-created", "-id"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Product<id={self.id}>"

    @property
    def calculated_price(self):
        discount = self.discount_set.filter(activated=True).aggregate(Max("value"))[
            "value__max"
        ]
        if discount is not None:
            return self.price * (1 - discount / 100)
        return self.price

    def as_dict(self):
        response_items = ["id", "name"]
        return {item: getattr(self, item) for item in response_items}


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart"

    def save(self, **kwargs):
        super(Cart, self).save(**kwargs)

    def recalculate(self):
        self.total = sum(entry.recalculate() for entry in self.entry_set.all())
        self.save()

    def __repr__(self):
        return f"Cart<id={self.id}>"


class Entry(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product, null=True, on_delete=models.CASCADE, related_name="products"
    )
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "entry"

    def save(self, **kwargs):
        previous_total = Decimal(self.total)
        self.total = self.quantity * self.product.calculated_price
        self.cart.total -= previous_total - self.total
        self.cart.updated = datetime.now()
        self.cart.save()
        super(Entry, self).save(**kwargs)

    def recalculate(self):
        self.total = self.quantity * self.product.calculated_price
        self.save()
        return self.total

    def delete(self, **kwargs):
        self.cart.total -= self.total
        self.cart.save()
        super(Entry, self).delete(**kwargs)

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.product.name)
