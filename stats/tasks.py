from django.utils import timezone

from celery import shared_task
from portfolio.models import PortfolioEntry, CashBalance
from stats.models import PortfolioValue
from django.contrib.auth import get_user_model
from portfolio.utils import fetch_stock_details, fetch_crypto_details
from config.settings.base import TZ


User = get_user_model()

@shared_task
def fetch_and_store_portfolio_values():
    """
    Fetches the current portfolio values for all users and stores them in the PortfolioValue model.
    """
    for user in User.objects.all():
        # Calculate total portfolio value
        total_value = 0
        cash_balance = CashBalance.objects.filter(user=user).first()
        if cash_balance:
            total_value += cash_balance.balance

        investments_value = 0
        portfolio_entries = PortfolioEntry.objects.filter(user=user)
        for entry in portfolio_entries:
            if entry.asset_type == 'stock':
                stock_details = fetch_stock_details(entry.asset_symbol)
                entry.current_price = stock_details['price']
                entry.current_value = entry.current_price * entry.quantity
            elif entry.asset_type == 'crypto':
                crypto_details = fetch_crypto_details(entry.asset_symbol)
                entry.current_price = crypto_details['price']
                entry.current_value = entry.current_price * entry.quantity

            investments_value += entry.current_value

        total_value += investments_value

        # Store the portfolio value
        now_utc4 = timezone.now().astimezone(TZ)  # Convert to UTC+4
        today = now_utc4.date()
        portfolio_value, created = PortfolioValue.objects.update_or_create(
            user=user,
            timestamp__date=today,  # Ensure only one record per day
            defaults={
                'total_value': total_value,
                'cash_balance': cash_balance.balance if cash_balance else 0,
                'investments_value': investments_value,
                'timestamp': now_utc4,
            }
        )

