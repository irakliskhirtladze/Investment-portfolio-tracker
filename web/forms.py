from django import forms
from web.choices import AssetType, TransactionType, CurrencyTransactionType
from web.validators import CustomValidators as cvs
from datetime import date



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
    """Used for cash balance correction and for initial setup/portfolio reset."""
    balance = forms.DecimalField(max_digits=20, decimal_places=2, initial=0, validators=[cvs.validate_non_negative], label="Cash Balance")


class AssetForm(forms.Form):
    """Used for initial setup/portfolio reset."""
    asset_type = forms.ChoiceField(choices=AssetType, label="Asset Type")
    asset_symbol = forms.CharField(max_length=10, label="Symbol")
    quantity = forms.DecimalField(max_digits=20, decimal_places=5, label="Quantity", validators=[cvs.validate_positive])
    average_trade_price = forms.DecimalField(max_digits=20, decimal_places=5, label="Average Price")


class AssetTransactionForm(forms.Form):
    date = forms.DateField(initial=date.today, validators=[cvs.validate_past], widget=forms.DateInput(attrs={'type': 'date'}))
    asset_type = forms.ChoiceField(choices=AssetType)
    symbol = forms.CharField(max_length=15)
    transaction_type = forms.ChoiceField(choices=TransactionType)
    quantity = forms.DecimalField(max_digits=20, decimal_places=5, validators=[cvs.validate_positive])
    trade_price = forms.DecimalField(max_digits=20, decimal_places=5, validators=[cvs.validate_positive])
    commission = forms.DecimalField(max_digits=20, decimal_places=5, validators=[cvs.validate_non_negative])


class CashTransactionForm(forms.Form):
    date = forms.DateField(initial=date.today, validators=[cvs.validate_past], widget=forms.DateInput(attrs={'type': 'date'}))
    transaction_type = forms.ChoiceField(choices=CurrencyTransactionType)
    quantity = forms.DecimalField(max_digits=20, decimal_places=5, validators=[cvs.validate_positive])
    commission = forms.DecimalField(max_digits=20, decimal_places=5, validators=[cvs.validate_non_negative])
