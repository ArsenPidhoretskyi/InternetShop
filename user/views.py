from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

from core.views import WithContextView
from .forms import RegisterForm, EditProfileForm


class SignUpView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/Signup.html"


class ProfileView(WithContextView):
    template_name = "registration/Profile.html"
    form_class = EditProfileForm

    def get(self, *args, **kwargs):
        user = self.request.user
        self.context["form"] = self.form_class(instance=user.profile)
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        user = self.request.user
        form = self.form_class(self.request.POST, instance=user.profile)
        self.context["form"] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("me"))
        return render(self.request, self.template_name, self.context)
