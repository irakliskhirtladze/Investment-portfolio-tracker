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


class CashBalanceForm(forms.Form):
    balance = forms.DecimalField(max_digits=20, decimal_places=2, initial=0, label="Cash Balance")


class AssetForm(forms.Form):
    ASSET_TYPE_CHOICES = [
        ('stock', 'Stock'),
        ('crypto', 'Crypto'),
    ]
    asset_type = forms.ChoiceField(choices=ASSET_TYPE_CHOICES, label="Asset Type")
    asset_symbol = forms.CharField(max_length=10, label="Symbol")
    quantity = forms.DecimalField(max_digits=20, decimal_places=5, label="Quantity")
    average_trade_price = forms.DecimalField(max_digits=20, decimal_places=5, label="Average Price")
