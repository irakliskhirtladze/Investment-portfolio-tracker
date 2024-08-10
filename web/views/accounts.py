from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.conf import settings
import requests
from web.forms import LoginForm, RegisterForm, ResendActivationForm
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

            if response.status_code == 200:  # Success
                data = response.json()
                access_token = data.get('access')
                refresh_token = data.get('refresh')

                response = redirect('dashboard')
                response.set_cookie('auth_token', access_token, httponly=True, secure=True)
                response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)
                return response
            else:
                # Handle authentication error
                error_detail = response.json().get('detail', '')
                if 'No active account found' in error_detail:
                    # User might not be registered or activated
                    register_url = reverse('register')
                    resend_activation_url = reverse('resend_activation')
                    print(f"Register URL: {register_url}")
                    print(f"Resend Activation URL: {resend_activation_url}")
                    messages.error(
                        request, 
                        f"Your account is either not registered or not activated. "
                        f"Please <a href='{register_url}'>register</a> or "
                        f"<a href='{resend_activation_url}'>resend activation email</a>."
                    )
                else:
                    messages.error(request, "Invalid credentials or unable to log in.")

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
            url = f"{settings.API_BASE_URL}/auth/users/resend_activation/"
            response = requests.post(url, data={'email': email})

            if response.status_code == 204:
                messages.success(request, "Activation email has been resent. Please check your inbox.")
                return redirect('login')
            else:
                messages.error(request, "An error occurred. Please check your email address and try again.")
        
        return render(request, self.template_name, {'form': form})
