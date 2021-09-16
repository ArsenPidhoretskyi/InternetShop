from django.db import models
from product.models import Product


class Discount(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.DecimalField(decimal_places=2, max_digits=4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "discount"

    def __repr__(self):
        return f"Discount<id={self.id}>"
