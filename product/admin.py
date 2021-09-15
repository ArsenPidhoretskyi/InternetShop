from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # date_hierarchy = "id"
    empty_value_display = "---"
    fields = ("id", "name", "description", "price", "available", "image")
    list_display = ("id", "name", "price", "available")
