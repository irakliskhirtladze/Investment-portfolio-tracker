from django.shortcuts import render, redirect
from portfolio.forms import StockTransactionForm, CryptoTransactionForm, CashTransactionForm
from portfolio.models import Portfolio, StockTransaction, CryptoTransaction, CashTransaction
from django.db.models import Sum
from portfolio.utils import PortfolioManager, TransactionManager


def show_portfolio(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    portfolio_manager = PortfolioManager(request.user)
    cash_balance = portfolio_manager.get_cash_balance()
    investment_value = portfolio.aggregate(total=Sum('current_value'))['total'] or 0
    total_portfolio_value = round(cash_balance.balance + investment_value, 2)

    return render(request,
                  'portfolio/portfolio.html',
                  {'portfolio': portfolio,
                   'cash_balance': cash_balance,
                   'total_portfolio_value': total_portfolio_value})


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
        portfolio_manager = PortfolioManager(request.user)
        investment_type = request.POST.get('investment_type')

        if investment_type == 'Stock':
            form_class = StockTransactionForm
        elif investment_type == 'Crypto':
            form_class = CryptoTransactionForm
        elif investment_type == 'Cash':
            form_class = CashTransactionForm
        else:
            return render(request, 'error.html', {'error_message': 'Invalid investment type'})

        form = form_class(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction_manager = TransactionManager(transaction.user)
            if not transaction_manager.is_transaction_valid(transaction, investment_type)[0]:
                return render(request,
                              'portfolio/transaction.html',
                              {'form': form,
                               'investment_type': investment_type,
                               'message': transaction_manager.is_transaction_valid(transaction, investment_type)[1]})

            elif transaction_manager.is_transaction_valid(transaction, investment_type)[0]:
                transaction.save()
                # Update portfolio based on transaction investment type
                if investment_type == 'Cash':
                    portfolio_manager.update_cash_balance(transaction)
                    return redirect('portfolio')
                elif investment_type in ('Stock', 'Crypto'):
                    portfolio_manager.update_portfolio(transaction, investment_type)
                    return redirect('portfolio')

        return render(request, 'portfolio/transaction.html', {'form': form,
                                                              'investment_type': investment_type})
