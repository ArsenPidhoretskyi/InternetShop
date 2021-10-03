from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin


class WithContextView(View):
    def __init__(self, **kwargs):
        super(WithContextView, self).__init__(**kwargs)
        self.context = dict()


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
