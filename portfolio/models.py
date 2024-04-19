from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from portfolio.choices import InstrumentType, TransactionType
from accounts.models import CustomUser as User
import pickle


def get_currency_choices():
    with open('portfolio/currencies.pkl', 'rb') as f:
        currency_choices = pickle.load(f)
    return tuple(currency_choices)


class PortfolioEntry(models.Model):
    """Stores portfolio entries. Fields are automatically calculated based on Transaction"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    date_modified = models.DateField(auto_now=True, verbose_name=_('Date Modified'))
    instrument_type = models.CharField(max_length=10, choices=InstrumentType.choices, verbose_name=_('Instrument Type'))
    instrument_symbol = models.CharField(max_length=10, verbose_name=_('Symbol'))
    instrument_name = models.CharField(max_length=100, verbose_name=_('Instrument Name'))
    trade_currency = models.CharField(max_length=5, choices=get_currency_choices(), verbose_name=_('Currency'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Instrument Quantity'))
    average_trade_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Trade Price'))
    commissions = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Commission'))
    cost_basis = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Cost Basis'))
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Current Price'))
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Current Value'))
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Profit/Loss'))
    profit_loss_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Profit/Loss %'))

    class Meta:
        verbose_name = _('Portfolio Entry')
        verbose_name_plural = _('Portfolio Entries')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Stores portfolio transactions made by user"""
    transaction_date = models.DateField(auto_now=True, verbose_name=_('Transaction Date'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    instrument_type = models.CharField(max_length=10, choices=InstrumentType.choices, verbose_name=_('Instrument Type'))
    instrument_symbol = models.CharField(max_length=10, verbose_name=_('Symbol'))
    instrument_name = models.CharField(max_length=100, verbose_name=_('Instrument Name'))

    transaction_currency = models.CharField(max_length=5,
                                            default='USD',
                                            choices=get_currency_choices(),
                                            verbose_name=_('Currency'))

    transaction_type = models.CharField(max_length=10,
                                        choices=TransactionType.choices,
                                        verbose_name=_('Transaction Type'))

    quantity = models.DecimalField(max_digits=20,
                                   decimal_places=5,
                                   validators=[MinValueValidator(0)],
                                   verbose_name=_('Quantity'))

    trade_price = models.DecimalField(max_digits=20,
                                      decimal_places=5,
                                      validators=[MinValueValidator(0)],
                                      verbose_name=_('Trade Price'))

    commission = models.DecimalField(max_digits=10,
                                     decimal_places=3,
                                     validators=[MinValueValidator(0)],
                                     verbose_name=_('Commission'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return str(self.instrument_symbol)
