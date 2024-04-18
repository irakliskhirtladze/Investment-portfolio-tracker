from django.db.models import TextChoices


class InstrumentType(TextChoices):
    STOCK = 'stocks', 'Stocks'
    CRYPTO = 'crypto', 'Crypto'
    CASH = 'cash', 'Cash'


class TransactionType(TextChoices):
    BUY = 'buy', 'Buy'
    SELL = 'sell', 'Sell'
    CASH_DEPOSIT = 'deposit', 'Cash Deposit'
    CASH_WITHDRAWAL = 'withdrawal', 'Cash Withdrawal'
