from django.urls import path
from stats.views import PortfolioStatsView

urlpatterns = [
    path('portfolio-stats/', PortfolioStatsView.as_view(), name='portfolio-stats'),
]
