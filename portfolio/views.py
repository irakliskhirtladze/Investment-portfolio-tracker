from django.shortcuts import render, redirect
from portfolio.forms import StockTransactionForm, CryptoTransactionForm, CashTransactionForm
from portfolio.models import Portfolio
from portfolio.utils import update_portfolio, check_transaction_form_data


def show_portfolio(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    return render(request, 'portfolio/portfolio.html', {'portfolio': portfolio})


def show_transaction_1(request):
    return render(request, 'portfolio/transaction_1.html')


def show_transaction_2(request):
    if request.method == 'POST':
        investment_type = request.POST.get('investment_type')
        print(f'Investment type: {investment_type}')
        if investment_type == 'Stock':
            form = StockTransactionForm(request.POST)
        elif investment_type == 'Crypto':
            form = CryptoTransactionForm(request.POST)
        elif investment_type == 'Cash':
            form = CashTransactionForm(request.POST)
        return render(request, 'portfolio/transaction_2.html', {'form': form, 'investment_type': investment_type})

    # form = StockTransactionForm()
    # return render(request, 'portfolio/transaction_2.html', {'form': form})


def save_transaction(request):
    pass
