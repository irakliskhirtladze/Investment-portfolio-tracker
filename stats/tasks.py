from celery import shared_task
from django.utils import timezone
from portfolio.models import PortfolioEntry, CashBalance
from stats.models import PortfolioValue


@shared_task
def fetch_and_store_portfolio_value():
    from accounts.models import CustomUser  # Import here to avoid circular import issues

    users = CustomUser.objects.all()
    for user in users:
        portfolio_entries = PortfolioEntry.objects.filter(user=user)
        cash_balance = CashBalance.objects.filter(user=user).first()

        if cash_balance:
            cash_balance_value = cash_balance.balance
        else:
            cash_balance_value = 0

        investments_value = sum(entry.current_value for entry in portfolio_entries)
        total_value = cash_balance_value + investments_value

        PortfolioValue.objects.update_or_create(
            user=user,
            date=timezone.now().date(),
            defaults={
                'total_value': total_value,
                'cash_balance': cash_balance_value,
                'investments_value': investments_value
            }
        )
