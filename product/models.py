from django.db import models


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.IntegerField()
    available = models.IntegerField()
    image = models.ImageField(upload_to="media/products")

    class Meta:
        db_table = "product"
