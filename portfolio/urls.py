from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portfolio.views import InitialSetupView, TransactionViewSet, PortfolioViewSet

router = DefaultRouter()
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('initial-setup/', InitialSetupView.as_view(), name='initial-setup'),
    path('', include(router.urls)),
]
