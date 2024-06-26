from django.shortcuts import render, redirect


def index(request):
    auth_token = request.session.get('auth_token')
    if not auth_token:
        return redirect('web_login')
    return render(request, 'web/portfolio/index.html', {'is_authenticated': True, 'is_homepage': True})


def transaction(request, portfolio_id):
    # Placeholder for future logic
    return render(request, 'web/portfolio/transaction.html', {'portfolio_id': portfolio_id})
