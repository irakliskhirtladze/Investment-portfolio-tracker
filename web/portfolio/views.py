from django.shortcuts import render, redirect


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'web/portfolio/index.html')


def transaction(request, portfolio_id):
    # Placeholder for future logic
    return render(request, 'web/portfolio/transaction.html', {'portfolio_id': portfolio_id})
