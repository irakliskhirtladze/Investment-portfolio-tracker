import random
from portfolio.models import Portfolio, CashBalance
import requests
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
    return random.randint(250, 270)


def get_crypto_price(crypto_name):
    """Retrieve the crypto price for the given symbol from CoinGecko API"""
    crypto_name = crypto_name.lower()
    # url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
    # response = requests.get(url)
    # data = response.json()
    # if crypto_name in data:
    #     return data[crypto_name]['usd']
    # else:
    #     return None
    return random.randint(55000, 70000)


# def check_transaction_form_data(form):
#     """Check form validity
#     and check if the financial instrument entered in form actually returns valid data from APIs"""
#     if form.is_valid():
#         if form.cleaned_data['instrument_type'] == 'stock':
#             if get_stock_price(form.cleaned_data['instrument_symbol']) is not None:
#                 return True
#         elif form.cleaned_data['instrument_type'] == 'crypto':
#             if get_crypto_price(form.cleaned_data['instrument_name']) is not None:
#                 return True
#     return False


# def update_portfolio(transaction):
#     """Update the portfolio based on the given transaction"""
#     # Retrieve the portfolio entry for the instrument symbol if it exists, otherwise create a new one
#     try:
#         portfolio_entry = Portfolio.objects.get(user=transaction.user,
#                                                 investment_symbol=transaction.instrument_symbol.upper())
#     except Exception:
#         portfolio_entry = Portfolio(
#             user=transaction.user,
#             instrument_type=transaction.instrument_type.lower().capitalize(),
#             instrument_symbol=transaction.instrument_symbol.upper(),
#             instrument_name=transaction.instrument_name.lower().capitalize(),
#             quantity=0,
#             average_trade_price=0,
#             commissions=0,
#             cost_basis=0,
#             current_price=0,
#             current_value=0,
#             profit_loss=0,
    #         profit_loss_percent=0
    #     )
    #
    # # Update portfolio entry based on the transaction type
    # if transaction.transaction_type == 'buy':
    #     portfolio_entry.quantity += transaction.quantity
    #     portfolio_entry.commissions += transaction.commission
    #     portfolio_entry.cost_basis += transaction.quantity * transaction.trade_price + transaction.commission
    #     portfolio_entry.average_trade_price = portfolio_entry.cost_basis / portfolio_entry.quantity
    #
    # elif transaction.transaction_type == 'sell':
    #     portfolio_entry.quantity -= transaction.quantity
    #     portfolio_entry.commissions += transaction.commission
    #     sale_proceed = transaction.trade_price * transaction.quantity - transaction.commission  # Temporary variable
    #     profit_loss = sale_proceed - portfolio_entry.cost_basis  # Temporary variable
    #     portfolio_entry.cost_basis -= profit_loss
    #     portfolio_entry.average_trade_price = portfolio_entry.cost_basis / portfolio_entry.quantity
    #
    # # Calculate current value and profit/loss of investments
    # if portfolio_entry.instrument_type == 'stock':
    #     portfolio_entry.current_price = Decimal(get_stock_price(portfolio_entry.instrument_symbol))
    # if portfolio_entry.instrument_type == 'crypto':
    #     portfolio_entry.current_price = Decimal(get_crypto_price(portfolio_entry.instrument_name))
    #
    # portfolio_entry.current_value = portfolio_entry.current_price * portfolio_entry.quantity
    # portfolio_entry.profit_loss = portfolio_entry.current_value - portfolio_entry.cost_basis
    # portfolio_entry.profit_loss_percent = portfolio_entry.profit_loss / portfolio_entry.cost_basis * 100
    #
    # # Save the updated portfolio entry and make a snapshot based on entries
    # portfolio_entry.save()


class PortfolioManager:
    """Manages portfolio entries"""
    def __init__(self, user):
        self.user = user
        self.portfolio = Portfolio.objects.filter(user=user)

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
        if investment_type == 'Stock':
            portfolio_entry, created = Portfolio.objects.get_or_create(
                user=self.user,
                investment_type=investment_type,
                investment_symbol=transaction.symbol.strip().upper(),
                defaults={'quantity': 0, 'average_trade_price': 0, 'commissions': 0, 'cost_basis': 0}
            )
            return portfolio_entry

        elif investment_type == 'Crypto':
            portfolio_entry, created = Portfolio.objects.get_or_create(
                user=self.user,
                investment_type=investment_type,
                investment_name=transaction.name.strip().lower().capitalize(),
                defaults={'quantity': 0, 'average_trade_price': 0, 'commissions': 0, 'cost_basis': 0}
            )
            return portfolio_entry

    def update_portfolio(self, transaction, investment_type):
        cash_balance = self.get_cash_balance()
        portfolio_entry = self.get_portfolio_entry(transaction, investment_type)

        if transaction.transaction_type == 'buy':
            trade_cost = transaction.quantity * transaction.trade_price + transaction.commission
            if trade_cost > cash_balance.balance:
                return False
            portfolio_entry.quantity += transaction.quantity
            portfolio_entry.commissions += transaction.commission
            portfolio_entry.cost_basis += transaction.quantity * transaction.trade_price + transaction.commission
            portfolio_entry.average_trade_price = portfolio_entry.cost_basis / portfolio_entry.quantity

            # Update cash balance
            cash_balance.balance -= trade_cost
            cash_balance.save()

        elif transaction.transaction_type == 'sell':
            if portfolio_entry.quantity > transaction.quantity:
                return False
            portfolio_entry.quantity -= transaction.quantity
            portfolio_entry.commissions += transaction.commission
            sale_proceed = transaction.trade_price * transaction.quantity - transaction.commission
            profit_loss = sale_proceed - portfolio_entry.cost_basis
            portfolio_entry.cost_basis -= profit_loss
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
