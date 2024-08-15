from django.db.models import TextChoices


class AssetType(TextChoices):
    STOCK = 'stock', 'Stock'
    CRYPTO = 'crypto', 'Crypto'


class TransactionType(TextChoices):
    BUY = 'buy', 'Buy'
    SELL = 'sell', 'Sell'


class CurrencyTransactionType(TextChoices):
    CASH_DEPOSIT = 'deposit', 'Cash Deposit'
    CASH_WITHDRAWAL = 'withdrawal', 'Cash Withdrawal'
    