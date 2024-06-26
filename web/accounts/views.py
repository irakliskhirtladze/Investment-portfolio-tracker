from django.shortcuts import render, redirect
import requests
from django.conf import settings


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        response = requests.post(f'{settings.API_BASE_URL}/auth/token/login/', data={'email': email, 'password': password})
        if response.status_code == 200:
            request.session['auth_token'] = response.json().get('auth_token')
            return redirect('index')
        else:
            return render(request, 'web/accounts/login.html', {'error': 'Invalid credentials', 'current_view': 'login'})
    return render(request, 'web/accounts/login.html', {'current_view': 'login'})


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        name = request.POST.get('name')
        response = requests.post(f'{settings.API_BASE_URL}/auth/users/', data={'email': email, 'password': password, 're_password': re_password, 'name': name})
        if response.status_code == 201:
            return redirect('login')
        else:
            return render(request, 'web/accounts/register.html', {'error': response.json(), 'current_view': 'register'})
    return render(request, 'web/accounts/register.html', {'current_view': 'register'})


def logout_view(request):
    auth_token = request.session.get('auth_token')
    if auth_token:
        requests.post(f'{settings.API_BASE_URL}/auth/token/logout/', headers={'Authorization': f'Token {auth_token}'})
        del request.session['auth_token']
    return redirect('index')
