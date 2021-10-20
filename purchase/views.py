from django.http import HttpResponseRedirect
from django.urls import reverse

from .services import create_purchase
from core.views import WithContextView


class CreatePurchase(WithContextView):
    def post(self, *args, **kwargs):
        create_purchase(self.request.user)
        return HttpResponseRedirect(reverse("me"))
