from decimal import Decimal, ROUND_HALF_UP, getcontext
import os
from dotenv import load_dotenv
import requests
from django.core.exceptions import ValidationError
from portfolio.choices import TransactionType, CurrencyTransactionType, TransactionCategory
from django.utils.translation import gettext_lazy as _

getcontext().prec = 10
load_dotenv()


def fetch_stock_price(symbol):
    api_key = os.getenv('FINNHUB_API_KEY')
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'

    response = requests.get(url)
    data = response.json()

    if 'c' in data and data['c'] > 0:
        return Decimal(str(data['c']))
    raise ValidationError({'current_price': _('Unable to fetch stock price for the given symbol.')})


def fetch_crypto_price(crypto_name):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd'

    response = requests.get(url)
    data = response.json()

    if crypto_name in data:
        return Decimal(str(data[crypto_name]['usd']))
    raise ValidationError({'current_price': _('Unable to fetch cryptocurrency price for the given name.')})


def calculate_portfolio_entry_fields(entry, refresh=False):
    """
    Calculates the fields for the given portfolio entry. Used during initial setup or refreshing.
    """
    if refresh or entry.current_price == Decimal('0.00'):
        if entry.investment_type == TransactionCategory.STOCK:
            entry.current_price = fetch_stock_price(entry.investment_symbol)
        elif entry.investment_type == TransactionCategory.CRYPTO:
            entry.current_price = fetch_crypto_price(entry.investment_name)

    entry.cost_basis = entry.average_trade_price * entry.quantity + entry.commissions
    entry.current_value = entry.current_price * entry.quantity
    entry.profit_loss = entry.current_value - entry.cost_basis
    entry.profit_loss_percent = (entry.profit_loss / entry.cost_basis) * 100 if entry.cost_basis != 0 else 0


def update_portfolio_entry(user, transaction):
    """
    Updates the portfolio entry for the given transaction.
    """
    from portfolio.models import PortfolioEntry, CashBalance

    portfolio_entry, created = PortfolioEntry.objects.get_or_create(
        user=user,
        investment_type=transaction.transaction_category,
        investment_symbol=transaction.symbol if transaction.transaction_category == TransactionCategory.STOCK
        else transaction.name,
        defaults={
            'investment_name': transaction.name if transaction.transaction_category == TransactionCategory.CRYPTO
            else transaction.symbol,
            'quantity': Decimal('0'), 'average_trade_price': Decimal('0')}
    )

    if transaction.transaction_type == TransactionType.BUY:
        new_total_quantity = portfolio_entry.quantity + transaction.quantity
        new_total_cost = ((portfolio_entry.quantity * portfolio_entry.average_trade_price) +
                          (transaction.quantity * transaction.trade_price))
        portfolio_entry.average_trade_price = ((new_total_cost / new_total_quantity).
                                               quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        portfolio_entry.quantity = new_total_quantity
    elif transaction.transaction_type == TransactionType.SELL:
        portfolio_entry.quantity -= transaction.quantity

    portfolio_entry.commissions += transaction.commission
    calculate_portfolio_entry_fields(portfolio_entry)
    portfolio_entry.save()


def update_cash_balance(user, transaction):
    """
    Updates the cash balance for the given transaction.
    """
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


def refresh_portfolio(user):
    """
    Refreshes the portfolio for the given user by getting updated current prices and recalculating fields.
    """
    from portfolio.models import PortfolioEntry

    portfolio_entries = PortfolioEntry.objects.filter(user=user)
    for entry in portfolio_entries:
        entry.current_price = fetch_stock_price(entry.investment_symbol) if \
            (entry.investment_type == TransactionCategory.STOCK) else fetch_crypto_price(entry.investment_name)
        calculate_portfolio_entry_fields(entry, refresh=True)
        entry.save()
