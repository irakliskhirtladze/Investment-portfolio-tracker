from django.urls import path
from django.contrib.auth.decorators import login_required
from web.views.accounts import LoginView, LogoutView, RegisterView, ActivateView, ResendActivationView
from web.views.portfolio import Dashboard, InitialSetup, AssetTransaction, CashTransaction


urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', login_required(LogoutView.as_view()), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/activate/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('accounts/resend-activation/', ResendActivationView.as_view(), name='resend_activation'),

    path('', login_required(Dashboard.as_view()), name='dashboard'),
    path('initial-setup/', login_required(InitialSetup.as_view()), name='initial-setup'),
    path('asset-transaction/', login_required(AssetTransaction.as_view()), name='asset-transaction'),
    path('cash-transaction/', login_required(CashTransaction.as_view()), name='cash-transaction'),
]