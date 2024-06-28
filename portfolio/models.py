from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from portfolio.choices import TransactionType, CurrencyTransactionType, TransactionCategory
from accounts.models import CustomUser as User


class InvestmentTransaction(models.Model):
    """Stores investment transactions made by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    transaction_date = models.DateTimeField(verbose_name=_('Transaction Date'))
    transaction_category = models.CharField(max_length=10,
                                            choices=TransactionCategory.choices,
                                            verbose_name=_('Transaction Category'))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Name'))
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
                                      null=True,
                                      blank=True,
                                      validators=[MinValueValidator(0)],
                                      verbose_name=_('Trade Price'))
    commission = models.DecimalField(max_digits=10,
                                     decimal_places=5,
                                     validators=[MinValueValidator(0)],
                                     verbose_name=_('Commission'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f"{self.transaction_category} - {self.name or self.symbol}"

    def clean(self):
        super().clean()
        if self.transaction_category == TransactionCategory.CRYPTO and not self.name:
            raise ValidationError({'name': _('Name is required for crypto transactions.')})
        if self.transaction_category == TransactionCategory.STOCK and not self.symbol:
            raise ValidationError({'symbol': _('Symbol is required for stock transactions.')})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class CashTransaction(models.Model):
    """Stores cash transactions made by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    transaction_date = models.DateTimeField(verbose_name=_('Transaction Date'))

    transaction_type = models.CharField(max_length=10,
                                        choices=CurrencyTransactionType.choices,
                                        verbose_name=_('Transaction Type'))

    amount = models.DecimalField(max_digits=20,
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
        return f"{self.transaction_type} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PortfolioEntry(models.Model):
    """A single portfolio entry. Fields are automatically calculated based on Transaction"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    investment_type = models.CharField(max_length=10, verbose_name=_('Investment Type'))
    investment_symbol = models.CharField(max_length=10, default='', verbose_name=_('Investment Symbol'))
    investment_name = models.CharField(max_length=100, default='', verbose_name=_('Investment Name'))
    quantity = models.DecimalField(max_digits=10, decimal_places=5, verbose_name=_('Investment Quantity'))

    average_trade_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Trade Price'))
    commissions = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Commission'))
    cost_basis = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Cost Basis'))
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
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=_('Cash Balance'))

    class Meta:
        verbose_name = _('Cash Balance')
        verbose_name_plural = _('Cash Balances')

    def __str__(self):
        return str(self.balance)
