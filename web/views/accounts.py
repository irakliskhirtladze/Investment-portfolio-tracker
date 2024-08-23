from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.conf import settings
import requests

from web.forms import LoginForm, RegisterForm, ResendActivationForm
from web.utils import redirect_authenticated_user, extract_and_add_error_messages

import http.client
import json


@method_decorator(redirect_authenticated_user, name='dispatch')
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            status_response = requests.post(f"{settings.API_BASE_URL}/auth/check-status/", data={'email': email})

            if status_response.status_code == 200:
                user_status = status_response.json().get('status')
                if user_status == 'active':
                    login_response = requests.post(f"{settings.API_BASE_URL}/auth/jwt/create/", data={
                        'email': email,
                        'password': password
                    })

                    if login_response.status_code == 200:
                        data = login_response.json()
                        access_token = data.get('access')
                        refresh_token = data.get('refresh')

                        response = redirect('dashboard')
                        response.set_cookie('auth_token', access_token, httponly=True, secure=True)
                        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)
                        return response
                    else:
                        messages.error(request, "Invalid credentials or unable to log in.")
                elif user_status == 'inactive':
                    resend_activation_url = reverse('resend_activation')
                    messages.error(
                        request, 
                        f"Your account is not activated. "
                        f"<a href='{resend_activation_url}'>Resend activation email</a>."
                    )
                elif user_status == 'unregistered':
                    register_url = reverse('register')
                    messages.error(
                        request, 
                        f"No account found with this email."
                    )
            else:
                messages.error(request, "Error checking user status. Please try again.")

        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        response = redirect('login')
        response.delete_cookie('auth_token')
        response.delete_cookie('refresh_token')
        messages.info(request, "You have been logged out.")
        return response


@method_decorator(redirect_authenticated_user, name='dispatch')
class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']

            if password != re_password:
                form.add_error('re_password', 'Passwords do not match')
                return render(request, self.template_name, {'form': form})

            # Make an API request to create a new user
            response = requests.post(f"{settings.API_BASE_URL}/auth/users/", data={
                'email': email,
                'password': password,
                're_password': re_password
            })

            if response.status_code == 201:
                messages.success(request, "Registration successful. Please check your email to activate your account.")
                return redirect('login')
            else:
                errors = response.json()
                extract_and_add_error_messages(request, errors)
        
        return render(request, self.template_name, {'form': form})


@method_decorator(redirect_authenticated_user, name='dispatch')
class ActivateView(View):
    def get(self, request, uidb64, token):
        # Send a request to the API to activate the user
        response = requests.get(f"{settings.API_BASE_URL}/auth/activate/{uidb64}/{token}/")

        if response.status_code == 200:
            return render(request, 'accounts/activation.html', {'success': True})
        else:
            return render(request, 'accounts/activation.html', {'success': False, 'errors': response.json()})


@method_decorator(redirect_authenticated_user, name='dispatch')
class ResendActivationView(View):
    template_name = 'accounts/resend_activation.html'

    def get(self, request):
        form = ResendActivationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            status_response = requests.post(f"{settings.API_BASE_URL}/auth/check-status/", data={'email': email})
            if status_response.status_code == 200:
                user_status = status_response.json().get('status')
                if user_status != 'inactive':
                    messages.error(request, "User with this email is either active or not yet registered.")
                    return redirect("resend_activation")

            url = f"{settings.API_BASE_URL}/auth/users/resend_activation/"
            response = requests.post(url, data={'email': email})

            if response.status_code == 204:
                messages.success(request, "Activation email has been resent. Please check your inbox.")
                return redirect('login')
            else:
                messages.error(request, "An error occurred. Please check your email address and try again.")
        
        return render(request, self.template_name, {'form': form})
