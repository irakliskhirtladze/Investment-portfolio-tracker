from django.urls import path
from accounts.views import ActivateUser


urlpatterns = [
    path('signup/', ActivateUser.as_view(), name='signup'),
]
