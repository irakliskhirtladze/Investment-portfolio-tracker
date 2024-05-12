from django.urls import path
from django.contrib.auth.decorators import login_required
from portfolio.views import show_portfolio, refresh_portfolio, show_transaction_page, save_transaction, all_transactions


urlpatterns = [
    path('', login_required(show_portfolio), name='portfolio'),
    path('portfolio', login_required(show_portfolio), name='portfolio'),
    path('portfolio/refresh', login_required(refresh_portfolio), name='refresh_portfolio'),
    path('portfolio/transaction', login_required(show_transaction_page), name='transaction'),
    path('portfolio/save_transaction/', login_required(save_transaction), name='save_transaction'),
    path('portfolio/transactions', login_required(all_transactions), name='transactions'),
]
