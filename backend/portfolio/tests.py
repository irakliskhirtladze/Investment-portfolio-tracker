import datetime
from decimal import Decimal, getcontext
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import CustomUser as User
from portfolio.models import PortfolioEntry, CashBalance
from portfolio.choices import TransactionCategory, TransactionType

getcontext().prec = 10


class PortfolioAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.initial_data = {
            "portfolio_entries": [
                {
                    "investment_type": TransactionCategory.STOCK,
                    "investment_symbol": "AAPL",
                    "investment_name": "Apple Inc.",
                    "quantity": Decimal('10'),
                    "average_trade_price": Decimal('150.00')
                }
            ],
            "cash_balance": {
                "balance": Decimal('1000.00')
            }
        }
        self.client.post("/api/v1/initial-setup/", self.initial_data, format='json')

    def assert_portfolio_entry(self, symbol, quantity, avg_price, cost_basis, commissions=None):
        portfolio_entry = PortfolioEntry.objects.get(user=self.user, investment_symbol=symbol)
        self.assertEqual(portfolio_entry.quantity, quantity)
        self.assertEqual(portfolio_entry.average_trade_price, avg_price)
        self.assertEqual(portfolio_entry.cost_basis, cost_basis)
        if commissions is not None:
            self.assertEqual(portfolio_entry.commissions, commissions)

    def assert_cash_balance(self, expected_balance):
        cash_balance = CashBalance.objects.get(user=self.user)
        self.assertEqual(cash_balance.balance, expected_balance)

    def test_initial_setup(self):
        self.assert_portfolio_entry("AAPL", Decimal('10'), Decimal('150.00'), Decimal('1500.00'))
        self.assert_cash_balance(Decimal('1000.00'))

    def test_buy_asset_not_enough_cash(self):
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 100,
            "trade_price": 200,
            "commission": 10
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sell_asset_not_enough_quantity(self):
        sell_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "symbol": "AAPL",
            "transaction_type": "sell",
            "quantity": 20,
            "trade_price": 200,
            "commission": 10
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', sell_transaction, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_stock_symbol_empty(self):
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "transaction_type": "buy",
            "quantity": 10,
            "trade_price": 150,
            "commission": 5
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_crypto_name_empty(self):
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "crypto",
            "symbol": "BTC",
            "transaction_type": "buy",
            "quantity": 1,
            "trade_price": 50000,
            "commission": 5
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_transaction_updates(self):
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": Decimal('5'),
            "trade_price": Decimal('160.00'),
            "commission": Decimal('10.00')
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_total_quantity = Decimal('15')  # 10 + 5
        new_total_cost = (
                    Decimal('150.00') * Decimal('10') + Decimal('160.00') * Decimal('5')).quantize(Decimal('0.01'))
        new_average_trade_price = (new_total_cost / new_total_quantity).quantize(Decimal('0.01'))
        new_cost_basis = (new_average_trade_price * new_total_quantity + Decimal('10.00')).quantize(Decimal('0.01'))
        self.assert_portfolio_entry("AAPL", new_total_quantity, new_average_trade_price, new_cost_basis)
        self.assert_cash_balance(Decimal('1000.00') - Decimal('5') * Decimal('160.00') - Decimal('10.00'))

    def test_sell_transaction_updates(self):
        sell_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "symbol": "AAPL",
            "transaction_type": "sell",
            "quantity": Decimal('5'),
            "trade_price": Decimal('155.00'),
            "commission": Decimal('5.00')
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', sell_transaction, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_total_quantity = Decimal('5')  # 10 - 5
        portfolio_entry = PortfolioEntry.objects.get(user=self.user, investment_symbol="AAPL")
        new_cost_basis = (portfolio_entry.average_trade_price * new_total_quantity + portfolio_entry.commissions).quantize(Decimal('0.01'))
        self.assert_portfolio_entry("AAPL", new_total_quantity, portfolio_entry.average_trade_price, new_cost_basis)
        self.assert_cash_balance(Decimal('1000.00') + Decimal('5') * Decimal('155.00') - Decimal('5.00'))

    def test_refresh_portfolio(self):
        """
        Checks that the portfolio entry fields are correctly updated after calling the endpoint.
        """
        response = self.client.post("/api/v1/portfolio/refresh/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        portfolio_entry = PortfolioEntry.objects.get(user=self.user, investment_symbol="AAPL")
        self.assertNotEqual(portfolio_entry.current_price, Decimal('0.00'))
        self.assertEqual(portfolio_entry.current_value, portfolio_entry.current_price * portfolio_entry.quantity)
        self.assertEqual(portfolio_entry.profit_loss, portfolio_entry.current_value - portfolio_entry.cost_basis)
        self.assertEqual(portfolio_entry.profit_loss_percent,
                         (portfolio_entry.profit_loss / portfolio_entry.cost_basis * 100).quantize(Decimal('0.01'))
                         if portfolio_entry.cost_basis != 0 else 0)

