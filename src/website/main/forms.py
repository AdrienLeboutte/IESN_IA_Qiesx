from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label= "Username", required=True, max_length=50)
    password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput)

class DirectionForm(forms.Form):
    direction = forms.CharField(label="Direction", required=True)

class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=250, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm Password", max_length=250, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="First Name", max_length=250, required=False)
    last_name = forms.CharField(label="Last Name", max_length=250, required=False)