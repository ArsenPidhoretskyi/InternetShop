from django import forms
from django.core.validators import ValidationError

from .models import Discount
from product.models import Product


class DiscountFrom(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(available__gt=0),
        label="Choose product",
        to_field_name="id",
        required=False,
        widget=forms.Select(attrs={"class": "browser-default"}),
    )
    url = forms.CharField(
        max_length=256,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(DiscountFrom, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def clean(self):
        url = self.cleaned_data["url"]
        product_select = self.cleaned_data["product"]
        if self.get_product() is None or (url and product_select is not None):
            raise ValidationError("One of field url/product need be filled")
        return self.cleaned_data

    def get_product(self):
        url = self.cleaned_data["url"]
        if url:
            host, product_id = url.split("/Products/", 2)
            return Product.objects.get(id=product_id)
        elif self.cleaned_data["product"] is not None:
            return self.cleaned_data["product"]

    def save(self, commit=True):
        product = self.get_product()
        entry = super(DiscountFrom, self).save(False)
        entry.product = product
        if commit:
            entry.save()
        return entry

    class Meta:
        model = Discount
        fields = ("value", "product")
