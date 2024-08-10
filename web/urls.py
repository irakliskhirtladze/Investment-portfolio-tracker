from django.urls import path
from web.views.accounts import LoginView, LogoutView, RegisterView, ActivateView
from web.views.portfolio import Dashboard
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', login_required(LogoutView.as_view()), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/activate/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='activate'),

    path('', login_required(Dashboard.as_view()), name='dashboard'),
]