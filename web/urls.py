from django.urls import path
from web.accounts import views as accounts_views
from web.portfolio import views as portfolio_views


urlpatterns = [
    path('', portfolio_views.index, name='index'),
    path('login/', accounts_views.login_view, name='login'),
    path('register/', accounts_views.register_view, name='register'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('portfolio/<int:portfolio_id>/', portfolio_views.transaction, name='transaction'),
]
