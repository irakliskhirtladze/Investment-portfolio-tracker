from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from portfolio.choices import InstrumentType, TransactionType, TransactionCurrency
from accounts.models import CustomUser as User
import pickle


def get_currency_choices():
    with open('portfolio/currencies.pkl', 'rb') as f:
        currency_choices = pickle.load(f)
    return tuple(currency_choices)


class Portfolio(models.Model):
    """Stores portfolio entries. Fields are automatically calculated based on Transaction"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    date_modified = models.DateField(auto_now=True, verbose_name=_('Date Modified'))
    investment_type = models.CharField(max_length=10, verbose_name=_('Investment Type'))
    investment_symbol = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Investment Symbol'))
    investment_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Investment Name'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Investment Quantity'))

    average_trade_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Trade Price'))
    commissions = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Commission'))
    cost_basis = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Cost Basis'))
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Current Price'))
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Current Value'))
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('P&L'))
    profit_loss_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('P&L %'))

    class Meta:
        verbose_name = _('Portfolio Entry')
        verbose_name_plural = _('Portfolio Entries')

    def __str__(self):
        return self.investment_type


class CashBalance(models.Model):
    """Stores portfolio entries. Fields are automatically calculated based on Transaction"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    date_modified = models.DateField(auto_now=True, verbose_name=_('Date Modified'))
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=_('Cash Balance'))

    class Meta:
        verbose_name = _('Cash Balance')
        verbose_name_plural = _('Cash Balances')

    def __str__(self):
        return str(self.balance)


class CashTransaction(models.Model):
    """Stores cash transactions made by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    transaction_date = models.DateTimeField(auto_now=True, verbose_name=_('Transaction Date'))

    transaction_type = models.CharField(max_length=10,
                                        choices=TransactionCurrency.choices,
                                        verbose_name=_('Transaction Type'))

    quantity = models.DecimalField(max_digits=20,
                                   decimal_places=2,
                                   validators=[MinValueValidator(0)],
                                   verbose_name=_('Quantity'))

    commission = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     validators=[MinValueValidator(0)],
                                     verbose_name=_('Commission'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return self.transaction_type


class CryptoTransaction(models.Model):
    """Stores crypto transactions made by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    transaction_date = models.DateTimeField(auto_now=True, verbose_name=_('Transaction Date'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    symbol = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Symbol'))

    transaction_type = models.CharField(max_length=10,
                                        choices=TransactionType.choices,
                                        verbose_name=_('Transaction Type'))

    quantity = models.DecimalField(max_digits=20,
                                   decimal_places=5,
                                   validators=[MinValueValidator(0)],
                                   verbose_name=_('Quantity'))

    trade_price = models.DecimalField(max_digits=10,
                                      decimal_places=5,
                                      validators=[MinValueValidator(0)],
                                      verbose_name=_('Trade Price'))

    commission = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     validators=[MinValueValidator(0)],
                                     verbose_name=_('Commission'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return self.name


class StockTransaction(models.Model):
    """Stores stock transactions made by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    transaction_date = models.DateTimeField(auto_now=True, verbose_name=_('Transaction Date'))
    symbol = models.CharField(max_length=10, verbose_name=_('Symbol'))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Name'))

    transaction_type = models.CharField(max_length=10,
                                        choices=TransactionType.choices,
                                        verbose_name=_('Transaction Type'))

    quantity = models.DecimalField(max_digits=20,
                                   decimal_places=2,
                                   validators=[MinValueValidator(0)],
                                   verbose_name=_('Quantity'))

    trade_price = models.DecimalField(max_digits=20,
                                      decimal_places=5,
                                      validators=[MinValueValidator(0)],
                                      verbose_name=_('Trade Price'))

    commission = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     validators=[MinValueValidator(0)],
                                     verbose_name=_('Commission'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return self.symbol
