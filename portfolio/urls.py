from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portfolio.views import InvestmentTransactionViewSet, CashTransactionViewSet

router = DefaultRouter()
router.register(r'investment-transactions', InvestmentTransactionViewSet)
router.register(r'cash-transactions', CashTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
