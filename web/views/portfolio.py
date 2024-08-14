from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.conf import settings
from django.contrib import messages

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

        if refresh_response.status_code == 200:
            return self.get(request)  # Re-render the dashboard with the updated data

        # Handle any errors during the refresh process
        messages.error(request, "Failed to refresh portfolio. Please try again.")
        return self.get(request)
