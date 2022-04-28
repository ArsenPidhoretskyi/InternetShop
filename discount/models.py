from django.db import models
from product.models import Product


class Discount(models.Model):
    id = models.BigAutoField(primary_key=True)
    activated = models.BooleanField(default=True)
    value = models.DecimalField(decimal_places=2, max_digits=4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        db_table = "discount"

    def __repr__(self):
        return f"Discount<id={self.id}>"
