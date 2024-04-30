from django.contrib import admin
from portfolio.models import Portfolio, CashTransaction, StockTransaction, CryptoTransaction


admin.site.register(Portfolio)
admin.site.register(CashTransaction)
admin.site.register(StockTransaction)
admin.site.register(CryptoTransaction)
