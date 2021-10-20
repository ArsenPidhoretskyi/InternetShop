from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .services import create_order, get_orders
from core.views import WithContextView


class CreateOrderView(WithContextView):
    def post(self, *args, **kwargs):
        create_order(self.request.user)
        return HttpResponseRedirect(reverse("me"))


class PurchasesView(WithContextView):
    template_name = "purchase/History.html"

    def get(self, *args, **kwargs):
        self.context["orders"] = get_orders(self.request.user)
        return render(self.request, self.template_name, self.context)
