from rest_framework.routers import DefaultRouter
from portfolio.views import PortfolioViewSet

router = DefaultRouter()
router.register(r'portfolio', PortfolioViewSet, basename='author')

urlpatterns = router.urls
