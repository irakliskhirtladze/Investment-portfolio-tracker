from portfolio.tests.test_setup import TestSetup
from portfolio.models import InvestmentTransaction, CashTransaction, PortfolioEntry, CashBalance
from decimal import Decimal
from datetime import datetime
from django.core.exceptions import ValidationError

class ModelTests(TestSetup):
    def test_cash_balance_creation(self):
        cash_balance = CashBalance.objects.create(user=self.user, balance=Decimal('1000.00'))
        self.assertEqual(cash_balance.balance, Decimal('1000.00'))
        self.assertEqual(str(cash_balance), '1000.00')

    def test_investment_transaction_creation(self):
        transaction = InvestmentTransaction.objects.create(
            user=self.user,
            transaction_date=datetime.now(),
            asset_type='stock',
            symbol='AAPL',
            transaction_type='buy',
            quantity=Decimal('10.00000'),
            trade_price=Decimal('150.00'),
            commission=Decimal('1.00')
        )
        self.assertEqual(transaction.symbol, 'AAPL')
        self.assertEqual(str(transaction), 'stock - AAPL')

    def test_cash_transaction_creation(self):
        transaction = CashTransaction.objects.create(
            user=self.user,
            transaction_date=datetime.now(),
            transaction_type='deposit',
            amount=Decimal('500.00'),
            commission=Decimal('0.50')
        )
        self.assertEqual(transaction.amount, Decimal('500.00'))
        self.assertEqual(str(transaction), 'deposit - 500.00')

    def test_portfolio_entry_creation(self):
        entry = PortfolioEntry.objects.create(
            user=self.user,
            asset_type='crypto',
            asset_symbol='BTC',
            asset_name='Bitcoin',
            quantity=Decimal('2.00000'),
            average_trade_price=Decimal('30000.00'),
            commissions=Decimal('10.00'),
            cost_basis=Decimal('60010.00'),
            current_price=Decimal('32000.00'),
            current_value=Decimal('64000.00'),
            profit_loss=Decimal('3990.00'),
            profit_loss_percent=Decimal('6.65')
        )
        self.assertEqual(entry.asset_symbol, 'BTC')
        self.assertEqual(str(entry), 'crypto - BTC')
