# from portfolio.models import Entry, CashBalance
# import requests
# from random import randint
from decimal import Decimal
import random

from django.core.exceptions import ValidationError

from portfolio.choices import TransactionType, CurrencyTransactionType


def get_fake_current_price(investment_symbol):
    """
    Generates a fake current price for the given investment symbol.
    In a real-world scenario, this would fetch the price from an external API.
    """
    # Generate a random price between 50 and 500 for demonstration purposes
    return Decimal(str(round(random.uniform(50, 500), 2)))


def calculate_portfolio_entry_fields(entry):
    entry.cost_basis = entry.average_trade_price * entry.quantity + entry.commissions
    entry.current_value = entry.current_price * entry.quantity
    entry.profit_loss = entry.current_value - entry.cost_basis
    entry.profit_loss_percent = (entry.profit_loss / entry.cost_basis) * 100 if entry.cost_basis != 0 else 0


def update_portfolio_entry(user, transaction):
    from portfolio.models import PortfolioEntry, CashBalance

    portfolio_entry, created = PortfolioEntry.objects.get_or_create(
        user=user,
        investment_type=transaction.transaction_category,
        investment_symbol=transaction.symbol,
        defaults={'investment_name': transaction.name, 'quantity': 0}
    )

    if transaction.transaction_type == TransactionType.BUY:
        new_total_quantity = portfolio_entry.quantity + transaction.quantity
        new_cost_basis = portfolio_entry.cost_basis + (transaction.quantity * transaction.trade_price) + transaction.commission
        portfolio_entry.average_trade_price = new_cost_basis / new_total_quantity
        portfolio_entry.quantity = new_total_quantity
    elif transaction.transaction_type == TransactionType.SELL:
        if portfolio_entry.quantity < transaction.quantity:
            raise ValidationError(f"Not enough {transaction.symbol} to sell.")
        portfolio_entry.quantity -= transaction.quantity

    portfolio_entry.commissions += transaction.commission
    portfolio_entry.save()


def update_cash_balance(user, transaction):
    from portfolio.models import CashBalance

    cash_balance, created = CashBalance.objects.get_or_create(user=user)
    if transaction.transaction_type == TransactionType.BUY:
        cash_balance.balance -= (transaction.quantity * transaction.trade_price) + transaction.commission
    elif transaction.transaction_type == TransactionType.SELL:
        cash_balance.balance += (transaction.quantity * transaction.trade_price) - transaction.commission
    elif transaction.transaction_type == CurrencyTransactionType.CASH_DEPOSIT:
        cash_balance.balance += transaction.amount - transaction.commission
    elif transaction.transaction_type == CurrencyTransactionType.CASH_WITHDRAWAL:
        if cash_balance.balance < transaction.amount + transaction.commission:
            raise ValidationError("Not enough balance to withdraw.")
        cash_balance.balance -= transaction.amount + transaction.commission

    cash_balance.save()


