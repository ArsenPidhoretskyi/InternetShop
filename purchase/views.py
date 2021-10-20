from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .services import create_purchase, get_purchases
from core.views import WithContextView


class CreatePurchaseView(WithContextView):
    def post(self, *args, **kwargs):
        create_purchase(self.request.user)
        return HttpResponseRedirect(reverse("me"))


class PurchasesView(WithContextView):
    template_name = "purchase/History.html"

    def get(self, *args, **kwargs):
        self.context["purchases"] = get_purchases(self.request.user)
        return render(self.request, self.template_name, self.context)
