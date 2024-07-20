import jwt
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from rest_framework_simplejwt.tokens import AccessToken

from portfolio.models import PortfolioEntry
from web.portfolio.forms import CashBalanceForm, PortfolioEntryFormSet
import requests
from django.conf import settings

User = get_user_model()


class IndexView(View):
    def get(self, request):
        auth_token = request.COOKIES.get('access_token')
        if not auth_token:
            return redirect('web_login')

        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.get(f'{settings.API_BASE_URL}/portfolio/', headers=headers)
        if response.status_code == 200:
            portfolio_data = response.json()
        else:
            portfolio_data = []

        print(f'USER: {request.user}')

        context = {
            'portfolio_data': portfolio_data,
            'is_authenticated': request.user.is_authenticated,
            'is_homepage': True,
            'user': request.user,
            'current_view': 'index'
        }
        return render(request, 'web/portfolio/index.html', context)


class InitialSetupView(View):
    def get(self, request):
        cash_balance_form = CashBalanceForm()
        portfolio_entry_formset = PortfolioEntryFormSet(queryset=PortfolioEntry.objects.none())
        return render(request, 'web/portfolio/initial_setup.html', {
            'cash_balance_form': cash_balance_form,
            'portfolio_entry_formset': portfolio_entry_formset,
            'current_view': 'initial_setup',
            'is_authenticated': request.user.is_authenticated,
            'user': request.user
        })

    def post(self, request):
        auth_token = request.COOKIES.get('access_token')
        if not auth_token:
            return redirect('web_login')

        headers = {'Authorization': f'Bearer {auth_token}'}

        cash_balance_form = CashBalanceForm(request.POST)
        portfolio_entry_formset = PortfolioEntryFormSet(request.POST)

        if cash_balance_form.is_valid() and portfolio_entry_formset.is_valid():
            cash_data = cash_balance_form.cleaned_data
            portfolio_data = [
                {
                    'investment_type': entry.cleaned_data['investment_type'],
                    'investment_symbol': entry.cleaned_data['investment_symbol'],
                    'investment_name': entry.cleaned_data['investment_name'],
                    'quantity': entry.cleaned_data['quantity'],
                    'average_trade_price': entry.cleaned_data['average_trade_price']
                }
                for entry in portfolio_entry_formset if entry.cleaned_data
            ]

            initial_setup_data = {
                'cash_balance': cash_data,
                'portfolio_entries': portfolio_data
            }

            response = requests.post(f'{settings.API_BASE_URL}/initial-setup/', json=initial_setup_data, headers=headers)

            if response.status_code == 200:
                return redirect('index')
            else:
                error_message = response.json().get('detail', 'An error occurred during initial setup.')
                return render(request, 'web/portfolio/initial_setup.html', {
                    'cash_balance_form': cash_balance_form,
                    'portfolio_entry_formset': portfolio_entry_formset,
                    'error': error_message
                })

        return render(request, 'web/portfolio/initial_setup.html', {
            'cash_balance_form': cash_balance_form,
            'portfolio_entry_formset': portfolio_entry_formset,

        })


class TransactionView(View):
    def get(self, request, portfolio_id):
        pass  # Implement transaction view


class RefreshPortfolioView(View):
    def get(self, request):
        auth_token = request.COOKIES.get('access_token')
        if not auth_token:
            return redirect('web_login')

        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.post(f'{settings.API_BASE_URL}/transactions/refresh-portfolio/', headers=headers)
        if response.status_code == 200:
            return redirect('index')
        else:
            return redirect('index', {'error': 'Unable to refresh portfolio'})
