from django.urls import path, include
from stats.views import PortfolioValueViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('portfolio-values', PortfolioValueViewSet, basename='portfolio-values')

urlpatterns = [
    path('', include(router.urls)),
]
