from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from portfolio.forms import TransactionForm
from portfolio.models import Transaction, PortfolioEntry


@login_required
def new_transaction(request):
    """Make a transaction for the logged in user. Buy or sell an instrument or get a cash deposit/withdrawal"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            print(transaction)
            transaction.save()

            # Update the portfolio
            # update_portfolio(transaction)

            return redirect('new_transaction')

    form = TransactionForm()
    return render(request, 'portfolio/new_transaction.html', {'form': form})


def update_portfolio(transaction):
    """Update the portfolio based on the given transaction"""
    # Retrieve or create the portfolio entry for the instrument
    portfolio_entry, created = PortfolioEntry.objects.get_or_create(
        user=transaction.user,
        instrument_symbol=transaction.instrument_symbol,
        defaults={
            'instrument_type': transaction.instrument_type,
            'instrument_name': transaction.instrument_name,
            'trade_currency': transaction.transaction_currency,
            'quantity': 0,  # Initialize quantity to 0 if it's a new entry
            'average_trade_price': 0,  # Initialize average trade price to 0 if it's a new entry
            'commissions': 0,  # Initialize commissions to 0 if it's a new entry
            'cost_basis': 0,  # Initialize cost basis to 0 if it's a new entry
        }
    )

    # Update portfolio entry based on the transaction type
    if transaction.transaction_type == 'BUY':
        # Update quantity, average trade price, commissions, and cost basis for buying transaction
        portfolio_entry.quantity += transaction.quantity
        portfolio_entry.average_trade_price = (
            (portfolio_entry.average_trade_price * (portfolio_entry.quantity - transaction.quantity)) +
            (transaction.trade_price * transaction.quantity)
        ) / portfolio_entry.quantity
        portfolio_entry.commissions += transaction.commission
        portfolio_entry.cost_basis += (transaction.trade_price * transaction.quantity) + transaction.commission
    elif transaction.transaction_type == 'SELL':
        # Update quantity and commissions for selling transaction
        portfolio_entry.quantity -= transaction.quantity
        portfolio_entry.commissions += transaction.commission

    # Save the updated portfolio entry
    portfolio_entry.save()


@login_required
def portfolio(request):
    """Get a current portfolio based on the transactions made"""
    pass

