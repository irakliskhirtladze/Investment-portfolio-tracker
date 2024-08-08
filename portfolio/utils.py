from decimal import Decimal, ROUND_HALF_UP, getcontext
import os
from django.conf import settings
import requests
from django.core.exceptions import ValidationError
from portfolio.choices import TransactionType, CurrencyTransactionType, AssetType
from django.utils.translation import gettext_lazy as _

getcontext().prec = 10


def fetch_stock_details(symbol):
    api_key = settings.FINNHUB_API_KEY
    symbol = symbol.upper()
    quote_url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'
    symbol_url = f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={api_key}'

    quote_response = requests.get(quote_url)
    quote_data = quote_response.json()

    if 'c' in quote_data and quote_data['c'] > 0:
        symbol_response = requests.get(symbol_url)
        symbol_data = symbol_response.json()

        if 'name' in symbol_data:
            return {
                'price': Decimal(str(quote_data['c'])),
                'name': symbol_data['name']
            }
        raise ValidationError({'name': _('Unable to fetch stock name for the given symbol.')})
    raise ValidationError({'current_price': _('Unable to fetch stock price for the given symbol.')})


def fetch_crypto_details(symbol):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol.upper()}&vs_currencies=usd'

    response = requests.get(url)
    data = response.json()

    if symbol in data:
        return {'price': Decimal(str(data[symbol]['usd'])),
                'name': symbol.capitalize()}
    raise ValidationError({'current_price': _('Unable to fetch cryptocurrency details for the given symbol.')})


def calculate_portfolio_entry_fields(entry, refresh=False):
    """
    Calculates the fields for the given portfolio entry. Used during initial setup or refreshing.
    """
    if refresh or entry.current_price == Decimal('0.00'):
        if entry.asset_type == AssetType.STOCK:
            entry.current_price = fetch_stock_details(entry.asset_symbol)['price']
        elif entry.asset_type == AssetType.CRYPTO:
            entry.current_price = fetch_crypto_details(entry.asset_symbol)['price']

    entry.cost_basis = entry.average_trade_price * entry.quantity + entry.commissions
    entry.current_value = entry.current_price * entry.quantity
    entry.profit_loss = entry.current_value - entry.cost_basis
    entry.profit_loss_percent = (entry.profit_loss / entry.cost_basis) * 100 if entry.cost_basis != 0 else 0


def update_portfolio_entry(user, transaction):
    """
    Updates the portfolio entry for the given transaction.
    """
    from portfolio.models import PortfolioEntry, CashBalance

    details = None
    if transaction.asset_type == AssetType.STOCK:
        details = fetch_stock_details(transaction.symbol)
    elif transaction.asset_type == AssetType.CRYPTO:
        details = fetch_crypto_details(transaction.symbol)

    portfolio_entry, created = PortfolioEntry.objects.get_or_create(
        user=user,
        asset_type=transaction.asset_type,
        asset_symbol=transaction.symbol,
        defaults={
            'asset_name': details['name'],
            'quantity': Decimal('0'),
            'average_trade_price': Decimal('0')
        }
    )

    if transaction.transaction_type == TransactionType.BUY:
        new_total_quantity = portfolio_entry.quantity + transaction.quantity
        new_total_cost = ((portfolio_entry.quantity * portfolio_entry.average_trade_price) +
                          (transaction.quantity * transaction.trade_price))
        portfolio_entry.average_trade_price = ((new_total_cost / new_total_quantity).
                                               quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP))
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
        if entry.asset_type == AssetType.STOCK:
            details = fetch_stock_details(entry.asset_symbol)
        elif entry.asset_type == AssetType.CRYPTO:
            details = fetch_crypto_details(entry.asset_symbol)

        entry.current_price = details['price']
        entry.asset_name = details['name']
        calculate_portfolio_entry_fields(entry, refresh=True)
        entry.save()
