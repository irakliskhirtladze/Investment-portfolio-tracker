from django import forms
from portfolio.models import CashBalance, PortfolioEntry
from django.forms import modelformset_factory


class CashBalanceForm(forms.ModelForm):
    class Meta:
        model = CashBalance
        fields = ['balance']


PortfolioEntryFormSet = modelformset_factory(
    PortfolioEntry,
    fields=('investment_type', 'investment_symbol', 'investment_name', 'quantity', 'average_trade_price'),
    extra=1,
    can_delete=False
)

