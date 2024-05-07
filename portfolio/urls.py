from django.urls import path
from django.contrib.auth.decorators import login_required
from portfolio.views import show_portfolio, show_transaction_page, save_transaction


urlpatterns = [
    path('portfolio', login_required(show_portfolio), name='portfolio'),
    path('portfolio/transaction', login_required(show_transaction_page), name='transaction'),
    path('portfolio/save_transaction/', login_required(save_transaction), name='save_transaction'),
]
