from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label= "Username", required=True, max_length=50)
    password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="First Name", max_length=250, required=False)
    last_name = forms.CharField(label="Last Name", max_length=250, required=False)

    class Meta:
        model = User
        fields = { "email", "username", "first_name", "last_name",}

    field_order = ["email", "username", "first_name", "last_name",]