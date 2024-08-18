from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.conf import settings
from django.contrib import messages

from web.forms import CashBalanceForm, AssetForm, AssetTransactionForm, CashTransactionForm
from web.utils import extract_and_add_error_messages

from decimal import Decimal
import requests


class Dashboard(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')

        cookies = request.COOKIES
        request_url = f"{settings.API_BASE_URL}/portfolio/"
        response = requests.get(request_url, headers={'Authorization': f'Bearer {cookies["auth_token"]}'})
        data = response.json()

        if response.status_code == 200:          
            context = {
                'user_email': user.email,
                'total_portfolio_value': Decimal(data['total_portfolio_value']),
                'cash_balance': Decimal(data['cash_balance']),
                'portfolio_entries': data['portfolio_entries'],
                }
            return render(request, 'portfolio/dashboard.html', context)
         
        return render(request, 'portfolio/dashboard.html', {'error': 'Unable to fetch portfolio data.'})
    
    def post(self, request):
        refresh_url = f"{settings.API_BASE_URL}/portfolio/refresh/"
        refresh_response = requests.post(refresh_url, headers={'Authorization': f'Bearer {request.COOKIES["auth_token"]}'})

        if refresh_response.status_code == 201:
            return self.get(request)  # Re-render the dashboard with the updated data

        # Handle any errors during the refresh process
        messages.error(request, "Failed to refresh portfolio. Please try again.")
        return self.get(request)


class InitialSetup(View):
    def get(self, request):
        return render(request, 'portfolio/initial_setup.html')

    def post(self, request):
        # Prepare cash balance
        cash_balance = request.POST.get('cash_balance', 0)
        cash_data = {"balance": float(cash_balance)}

        # Prepare portfolio entries
        portfolio_entries = []
        asset_types = request.POST.getlist('asset_type')
        asset_symbols = request.POST.getlist('asset_symbol')
        quantities = request.POST.getlist('quantity')
        average_trade_prices = request.POST.getlist('average_trade_price')

        for asset_type, asset_symbol, quantity, average_trade_price in zip(asset_types, asset_symbols, quantities, average_trade_prices):
            if asset_type and asset_symbol and quantity and average_trade_price:
                portfolio_entries.append({
                    "asset_type": asset_type,
                    "asset_symbol": asset_symbol,
                    "quantity": float(quantity),
                    "average_trade_price": float(average_trade_price)
                })

        data = {"cash_balance": cash_data, "portfolio_entries": portfolio_entries}

        response = requests.post(
            f"{settings.API_BASE_URL}/initial-setup/",
            json=data,
            headers={'Authorization': f'Bearer {request.COOKIES["auth_token"]}'}
        )

        if response.status_code == 201:
            messages.success(request, "Setup completed successfully!")
            return redirect('dashboard')
        else:
            errors = response.json()
            extract_and_add_error_messages(request, errors)
            return render(request, 'portfolio/initial_setup.html')
        
    
class AssetTransaction(View):
    def get(self, request):
        return render(request, 'portfolio/asset_transaction.html', {'form': AssetTransactionForm()})
    
    def post(self, request):
        form = AssetTransactionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.user.id
            data['transaction_date'] = data['transaction_date'].isoformat()

            for key, value in data.items():
                if isinstance(value, Decimal):
                    data[key] = str(value)

            response = requests.post(
                f"{settings.API_BASE_URL}/transactions/create-investment-transaction/",
                json=data,
                headers={"Authorization": f"Bearer {request.COOKIES['auth_token']}"}
            )
            
            print(response.status_code)
            if response.status_code == 201:
                messages.success(request, "Transaction created successfully!")
                return redirect('asset-transaction')
            else:
                errors = response.json()
                extract_and_add_error_messages(request, errors)
                return redirect('asset-transaction')
        
        else:
            messages.error(request, "There was an error with your submission. Please try again.")
        
        return render(request, 'portfolio/asset_transaction.html', {form: form})
                

class CashTransaction(View):
    def get(self, request):
        return render(request, 'portfolio/cash_transaction.html', {'form': CashTransactionForm()})
    
    def post(self, request):
        form = AssetTransactionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.user.id
            data['transaction_date'] = data['transaction_date'].isoformat()

            for key, value in data.items():
                if isinstance(value, Decimal):
                    data[key] = str(value)

            response = requests.post(
                f"{settings.API_BASE_URL}/transactions/create-cash-transaction/",
                json=data,
                headers={"Authorization": f"Bearer {request.COOKIES['auth_token']}"}
            )

            if response.status_code == 201:
                messages.success(request, "Transaction created successfully!")
                return redirect('cash-transaction')
            else:
                errors = response.json()
                extract_and_add_error_messages(request, errors)
                return redirect('cash-transaction')

        else:
            messages.error(request, "There was an error with your submission. Please try again.")

        return render(request, 'portfolio/cash_transaction.html', {form: form})
