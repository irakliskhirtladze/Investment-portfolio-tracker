from django.urls import path
from portfolio.views import portfolio, new_transaction


urlpatterns = [
    path('', portfolio, name='portfolio'),
    path('new_transaction/', new_transaction, name='new_transaction'),
]
