from django.db import models
from product.models import Product


class Discount(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.DecimalField(decimal_places=2, max_digits=3)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "discount"
