from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from portfolio.choices import TransactionCategory, TransactionType, CurrencyTransactionType


def validate_investment_transaction(transaction):
    from portfolio.models import PortfolioEntry, CashBalance

    if transaction.transaction_category == TransactionCategory.CRYPTO and not transaction.name:
        raise ValidationError({'name': _('Name is required for crypto transactions.')})
    if transaction.transaction_category == TransactionCategory.STOCK and not transaction.symbol:
        raise ValidationError({'symbol': _('Symbol is required for stock transactions.')})

    # Validate cash balance for buy transactions
    if transaction.transaction_type == TransactionType.BUY:
        cash_balance = CashBalance.objects.get(user=transaction.user).balance
        total_cost = transaction.quantity * transaction.trade_price + transaction.commission
        if total_cost > cash_balance:
            raise ValidationError({'cash_balance': _('Insufficient cash balance for this transaction.')})

    # Validate portfolio quantity for sell transactions
    if transaction.transaction_type == TransactionType.SELL:
        portfolio_entry = PortfolioEntry.objects.filter(
            user=transaction.user,
            investment_type=transaction.transaction_category,
            investment_symbol=transaction.symbol
        ).first()
        if not portfolio_entry:
            raise ValidationError({'portfolio_entry': _('You currently do not own this asset so it cannot be sold.')})
        if portfolio_entry and transaction.quantity > portfolio_entry.quantity:
            raise ValidationError({'quantity': _('Cannot sell more than the available quantity.')})


def validate_cash_transaction(transaction):
    from portfolio.models import CashBalance

    if transaction.transaction_type == CurrencyTransactionType.CASH_WITHDRAWAL:
        cash_balance = CashBalance.objects.get(user=transaction.user).balance
        total_cost = transaction.amount + transaction.commission
        if total_cost > cash_balance:
            raise ValidationError({'cash_balance': _('Insufficient cash balance for this withdrawal.')})
