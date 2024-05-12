from portfolio.models import Portfolio, CashBalance
import requests
from random import randint
from decimal import Decimal


def get_stock_price(symbol):
    """Retrieve the stock price for the given symbol from AlphaVantage API"""
    symbol = symbol.upper()
    # api_key = 'Y0LMWNXK9ED7IKCC'
    # url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    # response = requests.get(url)
    # data = response.json()
    # try:
    #     return data['Global Quote']['05. price']
    # except KeyError:
    #     return None
    return randint(19, 21)


def get_crypto_price(crypto_name):
    """Retrieve the crypto price for the given symbol from CoinGecko API"""
    crypto_name = crypto_name.lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if crypto_name in data:
        return data[crypto_name]['usd']
    else:
        return None
    # return randint(999, 1001)


class TransactionManager:
    """Manages a single transaction"""
    def __init__(self, user):
        self.user = user
        self.portfolio_manager = PortfolioManager(self.user)

    @staticmethod
    def get_buy_cost(transaction):
        return transaction.quantity * transaction.trade_price + transaction.commission

    def transaction_instrument_exists(self, transaction, investment_type):
        if investment_type == 'Stock':
            if self.portfolio_manager.get_portfolio_entry(transaction, 'Stock') is None:
                return False
        elif investment_type == 'Crypto':
            if self.portfolio_manager.get_portfolio_entry(transaction, 'Crypto') is None:
                return False
        return True

    def is_transaction_valid(self, transaction, investment_type):
        """Checks if transaction is valid and return a tuple of (True/False, message)"""
        if transaction.quantity < 0:
            return False, 'Quantity cannot be negative'
        if transaction.commission < 0:
            return False, 'Commission cannot be negative'

        cash_balance = self.portfolio_manager.get_cash_balance()

        if transaction.transaction_type == 'buy':
            if cash_balance.balance < self.get_buy_cost(transaction):
                return False, 'Insufficient funds to buy'

        elif transaction.transaction_type == 'sell':
            if not self.transaction_instrument_exists(transaction, investment_type):
                return False, 'Instrument does not exist'

            portfolio_entry = self.portfolio_manager.get_portfolio_entry(transaction, investment_type)
            if portfolio_entry.quantity < transaction.quantity:
                return False, 'Insufficient quantity to sell'

        elif transaction.transaction_type == 'withdrawal':
            if cash_balance.balance < transaction.quantity:
                return False, 'Insufficient cash to withdraw'

        return True, 'Valid'


class PortfolioManager:
    """Manages portfolio entries"""
    def __init__(self, user):
        self.user = user

    def get_cash_balance(self):
        cash_balance, created = CashBalance.objects.get_or_create(user=self.user)
        return cash_balance

    def update_cash_balance(self, transaction):
        cash_balance = self.get_cash_balance()

        if transaction.transaction_type == 'deposit':
            cash_balance.balance += transaction.quantity - transaction.commission
            if len(str(cash_balance.balance)) > 15:
                return False
        elif transaction.transaction_type == 'withdrawal':
            cash_balance.balance -= transaction.quantity + transaction.commission
            if cash_balance.balance < 0:
                return False

        cash_balance.save()

    def get_portfolio_entry(self, transaction, investment_type):
        """Try to retrieve portfolio entry based on transaction and investment type.
        If it doesn't exist, return None"""
        try:
            if investment_type == 'Stock':
                filter_kwargs = {
                    'user': self.user,
                    'investment_type': investment_type,
                    'investment_symbol': transaction.symbol.strip().upper()
                }
            elif investment_type == 'Crypto':
                filter_kwargs = {
                    'user': self.user,
                    'investment_type': investment_type,
                    'investment_name': transaction.name.strip().lower().capitalize()
                }
            else:
                return None  # Invalid investment type

            portfolio_entry = Portfolio.objects.get(**filter_kwargs)
            return portfolio_entry
        except Exception:
            return None

    def create_portfolio_entry(self, transaction, investment_type):
        """Create portfolio entry and return it without saving to database"""
        if investment_type == 'Stock':
            portfolio_entry = Portfolio(
                user=self.user,
                investment_type=investment_type,
                investment_symbol=transaction.symbol.strip().upper(),
                quantity=0  # Initialize quantity to 0
            )
            return portfolio_entry

        elif investment_type == 'Crypto':
            portfolio_entry = Portfolio(
                user=self.user,
                investment_type=investment_type,
                investment_name=transaction.name.strip().lower().capitalize(),
                quantity=0  # Initialize quantity to 0
            )
            return portfolio_entry

    def update_portfolio(self, transaction, investment_type):
        """Update a portfolio entry based on transaction and investment type"""
        cash_balance = self.get_cash_balance()
        portfolio_entry = self.get_portfolio_entry(transaction, investment_type)
        if portfolio_entry is None:
            portfolio_entry = self.create_portfolio_entry(transaction, investment_type)

        if transaction.transaction_type == 'buy':
            trade_cost = transaction.quantity * transaction.trade_price + transaction.commission

            portfolio_entry.quantity += transaction.quantity
            portfolio_entry.commissions += transaction.commission
            portfolio_entry.cost_basis += trade_cost + transaction.commission
            portfolio_entry.average_trade_price = portfolio_entry.cost_basis / portfolio_entry.quantity

            # Update cash balance
            cash_balance.balance -= trade_cost
            cash_balance.save()

        elif transaction.transaction_type == 'sell':
            sale_proceed = transaction.trade_price * transaction.quantity - transaction.commission
            avg_cost_per_instrument = portfolio_entry.cost_basis / portfolio_entry.quantity
            cost_basis_for_sale = avg_cost_per_instrument * transaction.quantity
            remaining_cost_basis = portfolio_entry.cost_basis - cost_basis_for_sale
            cost_basis_per_remaining = remaining_cost_basis / (portfolio_entry.quantity - transaction.quantity)

            portfolio_entry.quantity -= transaction.quantity
            portfolio_entry.commissions += transaction.commission
            portfolio_entry.cost_basis = cost_basis_per_remaining * portfolio_entry.quantity + portfolio_entry.commissions
            portfolio_entry.average_trade_price = portfolio_entry.cost_basis / portfolio_entry.quantity

            # Update cash balance
            cash_balance.balance += sale_proceed
            cash_balance.save()

        # Get current price for the portfolio entry
        if investment_type == 'Stock':
            portfolio_entry.current_price = Decimal(get_stock_price(portfolio_entry.investment_symbol))
        elif investment_type == 'Crypto':
            portfolio_entry.current_price = Decimal(get_crypto_price(portfolio_entry.investment_name))

        portfolio_entry.current_value = portfolio_entry.current_price * portfolio_entry.quantity
        portfolio_entry.profit_loss = portfolio_entry.current_value - portfolio_entry.cost_basis
        portfolio_entry.profit_loss_percent = portfolio_entry.profit_loss / portfolio_entry.cost_basis * 100

        portfolio_entry.save()

    def refresh_portfolio(self):
        """Update current price for all portfolio entries and related metrics"""
        for portfolio_entry in Portfolio.objects.filter(user=self.user):
            if portfolio_entry.investment_type == 'Stock':
                portfolio_entry.current_price = Decimal(get_stock_price(portfolio_entry.investment_symbol))
            elif portfolio_entry.investment_type == 'Crypto':
                portfolio_entry.current_price = Decimal(get_crypto_price(portfolio_entry.investment_name))

            portfolio_entry.current_value = portfolio_entry.current_price * portfolio_entry.quantity
            portfolio_entry.profit_loss = portfolio_entry.current_value - portfolio_entry.cost_basis
            portfolio_entry.profit_loss_percent = portfolio_entry.profit_loss / portfolio_entry.cost_basis * 100
            portfolio_entry.save()
