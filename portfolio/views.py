from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from portfolio.forms import TransactionForm
from portfolio.models import PortfolioEntry
from portfolio.utils import update_portfolio, check_transaction_form_data


@login_required
def new_transaction(request):
    """Make a transaction for the logged-in user. Buy or sell an instrument or make a cash deposit/withdrawal"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if check_transaction_form_data(form):
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            update_portfolio(transaction)

            return redirect('new_transaction')

    form = TransactionForm()
    return render(request, 'portfolio/new_transaction.html', {'form': form})


@login_required
def portfolio(request):
    """Get a current portfolio based on the transactions made"""
    portfolio_entries = PortfolioEntry.objects.filter(user=request.user).order_by('quantity')

    return render(request, 'portfolio/portfolio.html', {'portfolio_entries': portfolio_entries})
