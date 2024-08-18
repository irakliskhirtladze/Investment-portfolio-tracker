import requests
import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib import messages


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


def extract_and_add_error_messages(request, errors):
    if isinstance(errors, dict):
        for value in errors.values():
            extract_and_add_error_messages(request, value)
    elif isinstance(errors, list):
        for item in errors:
            extract_and_add_error_messages(request, item)
    else:
        messages.error(request, errors)
