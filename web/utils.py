import requests
import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


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
