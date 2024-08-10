from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
import requests
from web.forms import LoginForm, RegisterForm
from web.utils import redirect_authenticated_user


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

            # Make an API request to authenticate
            response = requests.post(f"{settings.API_BASE_URL}/auth/jwt/create/", data={
                'email': email,
                'password': password
            })

            if response.status_code == 200:
                data = response.json()
                access_token = data.get('access')
                refresh_token = data.get('refresh')

                response = redirect('dashboard')
                response.set_cookie('auth_token', access_token, httponly=True, secure=True)
                response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)
                return response
            else:
                messages.error(request, "Invalid credentials or unable to log in")

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
                for field, error in errors.items():
                    form.add_error(field, error)
        
        return render(request, self.template_name, {'form': form})


class ActivateView(View):
    def get(self, request, uidb64, token):
        # Send a request to the API to activate the user
        response = requests.get(f"{settings.API_BASE_URL}/auth/activate/{uidb64}/{token}/")

        if response.status_code == 200:
            return render(request, 'accounts/activation.html', {'success': True})
        else:
            return render(request, 'accounts/activation.html', {'success': False, 'errors': response.json()})
