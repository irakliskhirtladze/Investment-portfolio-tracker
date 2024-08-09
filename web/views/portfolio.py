from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from config.settings.base import API_BASE_URL


class Dashboard(View):
    def get(self, request):
        if not request.is_authenticated:
            print("User not authenticated, redirecting to login")  # Debug print
            return redirect('login')
        print("User authenticated, rendering dashboard")  # Debug print
        return render(request, 'portfolio/dashboard.html')

