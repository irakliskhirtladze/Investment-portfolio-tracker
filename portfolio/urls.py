from django.urls import path
from django.contrib.auth.decorators import login_required
from portfolio.views import show_portfolio, show_transaction_1, show_transaction_2,\
    save_transaction


urlpatterns = [
    path('portfolio', login_required(show_portfolio), name='portfolio'),

    path('portfolio/transaction_pg_1', login_required(show_transaction_1), name='transaction_pg_1'),
    path('portfolio/transaction_pg_2', login_required(show_transaction_2), name='transaction_pg_2'),
    path('portfolio/save_transaction/', login_required(save_transaction), name='save_transaction'),
]
