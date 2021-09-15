from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()


class Purchase(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "purchase"

    def __repr__(self):
        return f"Purchase<id={self.id}>"