from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
            )
            profile.save()
        return user


class EditProfileForm(forms.ModelForm, forms.Form):
    email = forms.CharField(max_length=128, widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        self.instance.user.email = self.cleaned_data["email"]
        super(EditProfileForm, self).save(commit)
        if commit:
            self.instance.user.save()
        return self.instance

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone_number"]
