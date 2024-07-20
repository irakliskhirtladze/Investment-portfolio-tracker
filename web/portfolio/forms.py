from django import forms
from django.forms import modelformset_factory
from portfolio.models import CashBalance, PortfolioEntry


class CashBalanceForm(forms.ModelForm):
    class Meta:
        model = CashBalance
        fields = ['balance']


class PortfolioEntryForm(forms.ModelForm):
    class Meta:
        model = PortfolioEntry
        fields = ['asset_type', 'asset_symbol', 'asset_name', 'quantity', 'average_trade_price']


PortfolioEntryFormSet = modelformset_factory(
    PortfolioEntry,
    form=PortfolioEntryForm,
    fields=('asset_type', 'asset_symbol', 'asset_name', 'quantity', 'average_trade_price'),
    extra=1,
    can_delete=True
)

