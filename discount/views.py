from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from core.views import WithContextView, SuperuserRequiredMixin, View
from . import services
from .forms import DiscountFrom


class DiscountsView(WithContextView):
    template_name = "discount/Discounts.html"

    def get(self, request, *args, **kwargs):
        self.context["discounts"] = services.get_discounts(request.user)
        return render(request, self.template_name, self.context)


class DiscountCreateView(SuperuserRequiredMixin, WithContextView):
    template_name = "discount/CreateDiscount.html"
    form_class = DiscountFrom

    def get(self, request, *args, **kwargs):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect(reverse("discount", args=(entry.id,)))
        self.context["form"] = form
        return render(self.request, self.template_name, self.context)


class DiscountView(WithContextView):
    template_name = "discount/Discount.html"

    def get(self, request, identifier: int, *args, **kwargs):
        self.context["discount"] = services.get_discount(identifier)
        return render(request, "discount/Discount.html", self.context)


class DiscountStatusView(View):
    def post(self, *args, **kwargs):
        discount_id = self.request.POST["id"]
        new_status = self.request.POST["status"].lower() == "true"
        services.change_status(discount_id, new_status)
        return JsonResponse({})
