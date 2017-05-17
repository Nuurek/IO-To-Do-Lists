from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(min_length=4)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), min_length=6)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def is_valid(self):
        valid = super(UserForm, self).is_valid()
        if not valid:
            return False
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        if password != confirm_password:
            self._errors["password"] = ["Password do not match"]
            return False
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            self._errors["email"] = ["Email address already in use"]
            return False
        return True
