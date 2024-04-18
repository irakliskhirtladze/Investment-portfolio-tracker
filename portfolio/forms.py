from django import forms
from portfolio.models import Transaction
from django.core.exceptions import ValidationError


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['user', 'transaction_date']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise ValidationError("Quantity must be a positive number.")
        return quantity

    def clean_trade_price(self):
        trade_price = self.cleaned_data.get('trade_price')
        if trade_price is not None and trade_price < 0:
            raise ValidationError("Trade price must be a positive number.")
        return trade_price

    def clean_commission(self):
        commission = self.cleaned_data.get('commission')
        if commission is not None and commission < 0:
            raise ValidationError("Commission must be a positive number.")
        return commission
