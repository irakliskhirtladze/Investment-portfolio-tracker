from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from portfolio.choices import TransactionType, TransactionCategory, CurrencyTransactionType
from portfolio.utils import fetch_stock_price, fetch_crypto_price


def validate_price_fetching(entry):
    if entry.investment_type == TransactionCategory.STOCK:
        if not entry.investment_symbol.isupper():
            raise ValidationError({'investment_symbol': _('Stock symbol must be uppercase.')})
        price = fetch_stock_price(entry.investment_symbol)
        if price is None:
            raise ValidationError({'current_price': _('Unable to fetch stock price for the given symbol.')})
    elif entry.investment_type == TransactionCategory.CRYPTO:
        if not entry.investment_name.islower():
            raise ValidationError({'investment_name': _('Crypto name must be lowercase.')})
        price = fetch_crypto_price(entry.investment_name)
        if price is None:
            raise ValidationError({'current_price': _('Unable to fetch cryptocurrency price for the given name.')})


def validate_initial_setup(entry):
    if entry.investment_type == TransactionCategory.STOCK:
        if not entry.investment_symbol:
            raise ValidationError({'investment_symbol': _('Symbol is required for stock entries.')})
        validate_price_fetching(entry)
    elif entry.investment_type == TransactionCategory.CRYPTO:
        if not entry.investment_name:
            raise ValidationError({'investment_name': _('Name is required for crypto entries.')})
        validate_price_fetching(entry)


def validate_investment_transaction(transaction):
    from portfolio.models import PortfolioEntry, CashBalance

    if transaction.transaction_category == TransactionCategory.STOCK:
        if not transaction.symbol:
            raise ValidationError({'symbol': _('Symbol is required for stock transactions.')})
    elif transaction.transaction_category == TransactionCategory.CRYPTO:
        if not transaction.name:
            raise ValidationError({'name': _('Name is required for crypto transactions.')})

    validate_price_fetching(transaction)

    if transaction.transaction_type == TransactionType.BUY:
        cash_balance = CashBalance.objects.get(user=transaction.user).balance
        total_cost = transaction.quantity * transaction.trade_price + transaction.commission
        if total_cost > cash_balance:
            raise ValidationError({'cash_balance': _('Insufficient cash balance for this transaction.')})

    if transaction.transaction_type == TransactionType.SELL:
        portfolio_entry = PortfolioEntry.objects.filter(
            user=transaction.user,
            investment_type=transaction.transaction_category,
            investment_symbol=transaction.symbol if transaction.transaction_category == TransactionCategory.STOCK else transaction.name
        ).first()
        if not portfolio_entry:
            raise ValidationError({'portfolio_entry': _('You currently do not own this asset so it cannot be sold.')})
        if transaction.quantity > portfolio_entry.quantity:
            raise ValidationError({'quantity': _('Cannot sell more than the available quantity.')})


def validate_cash_transaction(transaction):
    from portfolio.models import CashBalance

    if transaction.transaction_type == CurrencyTransactionType.CASH_WITHDRAWAL:
        cash_balance = CashBalance.objects.get(user=transaction.user).balance
        if transaction.amount + transaction.commission > cash_balance:
            raise ValidationError({'cash_balance': _('Not enough balance to withdraw.')})
