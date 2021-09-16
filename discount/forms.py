from django import forms
from .models import Discount
from product.models import Product


class DiscountFrom(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(available__gt=0),
        label="Choose product",
        to_field_name="id",
        required=True,
        widget=forms.Select(attrs={"class": "browser-default"}),
    )

    class Meta:
        model = Discount
        fields = ("value", "product")
