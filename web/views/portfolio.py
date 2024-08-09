from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.conf import settings
import requests


class Dashboard(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'portfolio/dashboard.html')

