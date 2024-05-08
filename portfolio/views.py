from django.shortcuts import render, redirect
from portfolio.forms import StockTransactionForm, CryptoTransactionForm, CashTransactionForm
from portfolio.models import Portfolio, StockTransaction, CryptoTransaction, CashTransaction
from django.db.models import Sum
from portfolio.utils import PortfolioManager


def show_portfolio(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    portfolio_manager = PortfolioManager(request.user)
    cash_balance = portfolio_manager.get_cash_balance()
    investment_value = portfolio.aggregate(total=Sum('current_value'))['total'] or 0
    total_portfolio_value = cash_balance.balance + investment_value

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

            # Update portfolio based on transaction
            if investment_type == 'Cash':
                cash_balance = portfolio_manager.update_cash_balance(transaction)
                if cash_balance is False:
                    return render(request, 'portfolio/transaction.html', {'form': form,
                                                                          'investment_type': investment_type})
                return redirect('portfolio')

            elif investment_type == 'Stock':
                updated_portfolio = portfolio_manager.update_portfolio(transaction, investment_type)
                if updated_portfolio is False:
                    return render(request, 'portfolio/transaction.html', {'form': form,
                                                                          'investment_type': investment_type})
                return redirect('portfolio')

            elif investment_type == 'Crypto':
                updated_portfolio = portfolio_manager.update_portfolio(transaction, investment_type)
                if updated_portfolio is False:
                    return render(request, 'portfolio/transaction.html', {'form': form,
                                                                          'investment_type': investment_type})
                return redirect('portfolio')

        return render(request, 'portfolio/transaction.html', {'form': form,
                                                              'investment_type': investment_type})
