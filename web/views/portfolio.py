from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.conf import settings
import requests


class Dashboard(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        cookies = request.COOKIES
        request_url = f"{settings.API_BASE_URL}/portfolio/"
        response = requests.get(request_url, headers={'Authorization': f'Bearer {cookies["auth_token"]}'})
        context = response.json()
        return render(request, 'portfolio/dashboard.html', context)
    
    
        
        

