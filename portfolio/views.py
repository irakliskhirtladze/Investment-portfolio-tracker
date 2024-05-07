from django.shortcuts import render, redirect
from portfolio.forms import StockTransactionForm, CryptoTransactionForm, CashTransactionForm
from portfolio.models import Portfolio, StockTransaction, CryptoTransaction, CashTransaction
from portfolio.utils import update_portfolio, check_transaction_form_data


def show_portfolio(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    return render(request, 'portfolio/portfolio.html', {'portfolio': portfolio})


def show_transaction_page(request):
    if request.method == 'POST':
        investment_type = request.POST.get('investment_type')
        if investment_type == 'Stock':
            form = StockTransactionForm(request.POST)
        elif investment_type == 'Crypto':
            form = CryptoTransactionForm(request.POST)
        elif investment_type == 'Cash':
            form = CashTransactionForm(request.POST)
        return render(request, 'portfolio/transaction.html', {'form': form, 'investment_type': investment_type})

    form = StockTransactionForm()
    return render(request, 'portfolio/transaction.html', {'form': form})


def save_transaction(request):
    """Saves transaction data in appropriate table based on investment type and updates portfolio"""
    if request.method == 'POST':
        investment_type = request.POST.get('investment_type')

        if investment_type == 'Stock':
            form_class = StockTransactionForm
            model_class = StockTransaction
        elif investment_type == 'Crypto':
            form_class = CryptoTransactionForm
            model_class = CryptoTransaction
        elif investment_type == 'Cash':
            form_class = CashTransactionForm
            model_class = CashTransaction
        else:
            return render(request, 'error.html', {'error_message': 'Invalid investment type'})

        form = form_class(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            print(transaction)
            return redirect('portfolio')

        return redirect('portfolio')
