import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from accounts.models import CustomUser as User
from portfolio.models import PortfolioEntry, CashBalance


class PortfolioAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_initial_setup(self):
        initial_setup_data = {
            "portfolio_entries": [
                {
                    "investment_type": "stock",
                    "investment_symbol": "AAPL",
                    "investment_name": "Apple Inc.",
                    "quantity": 10,
                    "average_trade_price": 150.00
                },
                {
                    "investment_type": "crypto",
                    "investment_symbol": "BTC",
                    "investment_name": "Bitcoin",
                    "quantity": 0.5,
                    "average_trade_price": 40000.00
                }
            ],
            "cash_balance": {
                "balance": 1000.00
            }
        }
        response = self.client.post('/api/v1/initial-setup/', initial_setup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_transaction_updates(self):
        self.test_initial_setup()
        buy_transaction = {
            "transaction_date": datetime.datetime.now().isoformat(),
            "transaction_category": "stock",
            "symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 5,
            "trade_price": 155,
            "commission": 5
        }
        response = self.client.post('/api/v1/transactions/create-investment-transaction/', buy_transaction,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch updated portfolio entry and cash balance
        portfolio_entry = PortfolioEntry.objects.get(user=self.user, investment_symbol="AAPL")
        cash_balance = CashBalance.objects.get(user=self.user)

        self.assertEqual(portfolio_entry.quantity, 15)  # 10 from initial setup + 5 from buy transaction
        self.assertEqual(cash_balance.balance,
                         1000 - (5 * 155 + 5))  # Initial cash balance - (quantity * trade_price + commission)
