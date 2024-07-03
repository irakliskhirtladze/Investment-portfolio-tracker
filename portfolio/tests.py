import datetime
from decimal import Decimal, ROUND_HALF_UP, getcontext
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from accounts.models import CustomUser as User
from portfolio.models import PortfolioEntry, CashBalance
from portfolio.choices import TransactionCategory, TransactionType

getcontext().prec = 10


class PortfolioAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_initial_setup(self):
        initial_data = {
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

        response = self.client.post("/api/v1/initial-setup/", initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        portfolio_entry = PortfolioEntry.objects.get(user=self.user, investment_symbol="AAPL")
        cash_balance = CashBalance.objects.get(user=self.user)

        self.assertEqual(portfolio_entry.quantity, Decimal('10'))
        self.assertEqual(portfolio_entry.average_trade_price, Decimal('150.00'))
        self.assertEqual(cash_balance.balance, Decimal('1000.00'))

    def test_buy_asset_not_enough_cash(self):
        self.test_initial_setup()
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 100,
            "trade_price": 200,
            "commission": 10
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sell_asset_not_enough_quantity(self):
        self.test_initial_setup()
        sell_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "symbol": "AAPL",
            "transaction_type": "sell",
            "quantity": 20,
            "trade_price": 200,
            "commission": 10
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', sell_transaction,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_stock_symbol_empty(self):
        self.test_initial_setup()
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "transaction_type": "buy",
            "quantity": 10,
            "trade_price": 150,
            "commission": 5
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_crypto_name_empty(self):
        self.test_initial_setup()
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "crypto",
            "transaction_type": "buy",
            "quantity": 0.5,
            "trade_price": 40000,
            "commission": 10
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_transaction_updates(self):
        self.test_initial_setup()

        buy_transaction = {
            "transaction_category": TransactionCategory.STOCK,
            "symbol": "AAPL",
            "transaction_type": TransactionType.BUY,
            "quantity": Decimal('5'),
            "trade_price": Decimal('160.00'),
            "commission": Decimal('10.00'),
            "transaction_date": "2023-01-01T00:00:00Z"
        }

        response = self.client.post("/api/v1/transactions/create-investment-transaction/", buy_transaction,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        portfolio_entry = PortfolioEntry.objects.get(user=self.user, investment_symbol="AAPL")
        cash_balance = CashBalance.objects.get(user=self.user)

        new_total_quantity = Decimal('15')  # 10 + 5
        new_average_trade_price = ((Decimal('150.00') * Decimal('10') + Decimal('160.00') * Decimal(
            '5')) / new_total_quantity).quantize(Decimal('0.01'))
        new_cost_basis = (new_average_trade_price * new_total_quantity + Decimal('10.00')).quantize(Decimal('0.01'))

        self.assertEqual(portfolio_entry.quantity, new_total_quantity)
        self.assertEqual(portfolio_entry.average_trade_price, new_average_trade_price)
        self.assertEqual(portfolio_entry.cost_basis, new_cost_basis)
        self.assertEqual(cash_balance.balance, Decimal('1000.00') - Decimal('5') * Decimal('160.00') - Decimal('10.00'))

    def test_sell_transaction_updates(self):
        self.test_initial_setup()

        sell_transaction = {
            "transaction_category": TransactionCategory.STOCK,
            "symbol": "AAPL",
            "transaction_type": TransactionType.SELL,
            "quantity": Decimal('5'),
            "trade_price": Decimal('155.00'),
            "commission": Decimal('5.00'),
            "transaction_date": "2023-01-01T00:00:00Z"
        }

        response = self.client.post("/api/v1/transactions/create-investment-transaction/", sell_transaction,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        portfolio_entry = PortfolioEntry.objects.get(user=self.user, investment_symbol="AAPL")
        cash_balance = CashBalance.objects.get(user=self.user)

        new_total_quantity = Decimal('5')  # 10 - 5
        new_cost_basis = (
                    portfolio_entry.average_trade_price * new_total_quantity + portfolio_entry.commissions).quantize(
            Decimal('0.01'))

        self.assertEqual(portfolio_entry.quantity, new_total_quantity)
        self.assertEqual(portfolio_entry.cost_basis, new_cost_basis)
        self.assertEqual(cash_balance.balance, Decimal('1000.00') + Decimal('5') * Decimal('155.00') - Decimal('5.00'))



