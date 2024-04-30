from django import forms
from portfolio.models import CashTransaction, CryptoTransaction, StockTransaction
from django.core.exceptions import ValidationError


class CashTransactionForm(forms.ModelForm):
    class Meta:
        model = CashTransaction
        exclude = ['user']


class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        exclude = ['user']


class CryptoTransactionForm(forms.ModelForm):
    class Meta:
        model = CryptoTransaction
        exclude = ['user']

