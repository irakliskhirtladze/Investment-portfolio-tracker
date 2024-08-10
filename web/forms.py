from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    re_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


class ResendActivationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
