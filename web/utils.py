import requests
import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps


def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return None

    response = requests.post(f"{settings.API_BASE_URL}/auth/jwt/refresh/", data={
        'refresh': refresh_token
    })

    if response.status_code == 200:
        data = response.json()
        return data.get('access')
    else:
        return None


def redirect_authenticated_user(view_func):
    """Decorator to redirect authenticated users to the dashboard."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
