from django import forms
from .models import Product


class ContactForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "available", "image")
