from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from portfolio.choices import TransactionType, CurrencyTransactionType, TransactionCategory
from portfolio.validations import validate_investment_transaction, validate_cash_transaction
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
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices,
                                        verbose_name=_('Transaction Type'))
    quantity = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)],
                                   verbose_name=_('Quantity'))
    trade_price = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True,
                                      validators=[MinValueValidator(0)],
                                      verbose_name=_('Trade Price'))
    commission = models.DecimalField(max_digits=10, decimal_places=5, validators=[MinValueValidator(0)],
                                     verbose_name=_('Commission'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f"{self.transaction_category} - {self.name or self.symbol}"

    def clean(self):
        validate_investment_transaction(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.update_portfolio_entry()

    def update_portfolio_entry(self):
        portfolio_entry, created = PortfolioEntry.objects.get_or_create(
            user=self.user,
            investment_type=self.transaction_category,
            investment_symbol=self.symbol,
            defaults={'investment_name': self.name, 'quantity': 0}
        )
        if self.transaction_type == TransactionType.BUY:
            portfolio_entry.quantity += self.quantity
        elif self.transaction_type == TransactionType.SELL:
            portfolio_entry.quantity -= self.quantity

        portfolio_entry.save()
        self.update_cash_balance()

    def update_cash_balance(self):
        cash_balance, created = CashBalance.objects.get_or_create(user=self.user)
        if self.transaction_type == TransactionType.BUY:
            cash_balance.balance -= self.quantity * self.trade_price + self.commission
        elif self.transaction_type == TransactionType.SELL:
            cash_balance.balance += self.quantity * self.trade_price - self.commission

        cash_balance.save()


class CashTransaction(models.Model):
    """Stores cash transactions made by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    transaction_date = models.DateTimeField(verbose_name=_('Transaction Date'))
    transaction_type = models.CharField(max_length=10, choices=CurrencyTransactionType.choices,
                                        verbose_name=_('Transaction Type'))
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)],
                                 verbose_name=_('Quantity'))
    commission = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                     verbose_name=_('Commission'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

    def clean(self):
        validate_cash_transaction(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.update_cash_balance()

    def update_cash_balance(self):
        cash_balance, created = CashBalance.objects.get_or_create(user=self.user)
        if self.transaction_type == CurrencyTransactionType.CASH_DEPOSIT:
            cash_balance.balance += self.amount - self.commission
        elif self.transaction_type == CurrencyTransactionType.CASH_WITHDRAWAL:
            cash_balance.balance -= self.amount + self.commission

        cash_balance.save()


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
        return f"{self.investment_type} - {self.investment_symbol or self.investment_name}"


class CashBalance(models.Model):
    """Stores portfolio entries. Fields are automatically calculated based on Transaction"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name=_('Cash Balance'))

    class Meta:
        verbose_name = _('Cash Balance')
        verbose_name_plural = _('Cash Balances')

    def __str__(self):
        return str(self.balance)
