from django.urls import path
from web.accounts import views as accounts_views
from web.portfolio import views as portfolio_views
from web.portfolio.views import InitialSetupView

urlpatterns = [
    path('login/', accounts_views.login_view, name='web_login'),
    path('register/', accounts_views.register_view, name='web_register'),
    path('logout/', accounts_views.logout_view, name='web_logout'),
    path('auth/activate/<uid>/<token>/', accounts_views.activation_view, name='activate'),

    path('', portfolio_views.IndexView.as_view(), name='index'),
    path('initial-setup/', InitialSetupView.as_view(), name='initial_setup'),
    path('portfolio/<int:portfolio_id>/', portfolio_views.TransactionView.as_view(), name='transaction'),
    path('refresh/', portfolio_views.RefreshPortfolioView.as_view(), name='refresh_portfolio'),
]
