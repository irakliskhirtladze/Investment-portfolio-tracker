from django.urls import path, include
from accounts.views import ActivateUser, CheckUserStatus

urlpatterns = [
    path('activate/<uid>/<token>/', ActivateUser.as_view(), name='activate-user'),
    path('check-status/', CheckUserStatus.as_view(), name='check-user-status'),
]
