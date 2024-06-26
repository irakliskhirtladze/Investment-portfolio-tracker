from django.shortcuts import render, redirect
import requests
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timedelta


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        response = requests.post(f'{settings.API_BASE_URL}/auth/jwt/create/',
                                 data={'email': email, 'password': password})
        if response.status_code == 200:
            tokens = response.json()
            response = redirect('index')

            access_expires = datetime.utcnow() + timedelta(minutes=5)
            refresh_expires = datetime.utcnow() + timedelta(days=1)

            response.set_cookie('access_token',
                                tokens['access'],
                                httponly=True,
                                secure=True,
                                samesite='Lax',
                                expires=access_expires)
            response.set_cookie('refresh_token',
                                tokens['refresh'],
                                httponly=True,
                                secure=True,
                                samesite='Lax',
                                expires=refresh_expires)
            return response

        return render(request,
                      'web/accounts/login.html',
                      {'error': 'Invalid credentials', 'current_view': 'login', 'is_authenticated': False})

    return render(request, 'web/accounts/login.html', {'current_view': 'login', 'is_authenticated': False})


def logout_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        requests.post(f'{settings.API_BASE_URL}/auth/jwt/blacklist/', data={'refresh': refresh_token})
    response = redirect('web_login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        name = request.POST.get('name')
        response = requests.post(f'{settings.API_BASE_URL}/auth/users/',
                                 data={'email': email, 'password': password, 're_password': re_password, 'name': name})
        if response.status_code == 201:
            return redirect('web_login')
        return render(request, 'web/accounts/register.html', {'error': response.json(), 'current_view': 'register'})

    return render(request, 'web/accounts/register.html', {'current_view': 'register'})


def activation_view(request, uid, token):
    """Renders the activation page after the user has clicked on the activation link sent to their email"""
    payload = {'uid': uid, 'token': token}
    url = f"{settings.API_BASE_URL}/auth/users/activation/"
    response = requests.post(url, data=payload)

    if response.status_code == 204:
        return render(request, 'web/accounts/activation.html', {'success': True, 'is_activation_page': True})
    return render(request, 'web/accounts/activation.html', {'success': False, 'is_activation_page': True})
