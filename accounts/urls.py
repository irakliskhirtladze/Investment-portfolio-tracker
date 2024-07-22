from django.urls import path, include
from accounts.views import ActivateUser

urlpatterns = [
    path('activate/<uid>/<token>/', ActivateUser.as_view(), name='activate-user'),
]
