from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.conf import settings

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
        print(data)
        if response.status_code == 200:          
            context = {
                'user_email': user.email,
                'total_portfolio_value': Decimal(data['total_portfolio_value']),
                'cash_balance': Decimal(data['cash_balance']),
                'portfolio_entries': data['portfolio_entries'],
                }
            return render(request, 'portfolio/dashboard.html', context)
    
    
        
        

