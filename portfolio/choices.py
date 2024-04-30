from django.db.models import TextChoices


class InstrumentType(TextChoices):
    STOCK = 'stock', 'Stock'
    CRYPTO = 'crypto', 'Crypto'
    CASH = 'cash', 'Cash'


class TransactionType(TextChoices):
    BUY = 'buy', 'Buy'
    SELL = 'sell', 'Sell'


class TransactionCurrency(TextChoices):
    CASH_DEPOSIT = 'deposit', 'Cash Deposit'
    CASH_WITHDRAWAL = 'withdrawal', 'Cash Withdrawal'
