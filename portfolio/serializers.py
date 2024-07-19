from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from portfolio.choices import TransactionType, TransactionCategory, CurrencyTransactionType
from portfolio.models import InvestmentTransaction, CashTransaction, PortfolioEntry, CashBalance


class InitialCashBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBalance
        fields = ['balance']

    def validate(self, data):
        if data['balance'] < 0:
            raise serializers.ValidationError("Cash balance cannot be a negative value.")
        return data


class InitialPortfolioEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEntry
        fields = ['investment_type', 'investment_symbol', 'investment_name', 'quantity', 'average_trade_price']

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if data['average_trade_price'] <= 0:
            raise serializers.ValidationError("Average trade price must be greater than 0.")
        if data['investment_type'] == TransactionCategory.STOCK and not data.get('investment_symbol'):
            raise serializers.ValidationError("Stock symbol is required for stocks.")
        if data['investment_type'] == TransactionCategory.CRYPTO and not data.get('investment_name'):
            raise serializers.ValidationError("Crypto name is required for crypto.")

        # Convert stock symbol to uppercase
        if data['investment_type'] == TransactionCategory.STOCK and data.get('investment_symbol'):
            data['investment_symbol'] = data['investment_symbol'].upper()

        # Convert crypto name to lowercase
        if data['investment_type'] == TransactionCategory.CRYPTO and data.get('investment_name'):
            data['investment_name'] = data['investment_name'].lower()

        return data


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentTransaction
        exclude = ('user',)

    def validate(self, data):
        user = self.context['request'].user

        # Ensure correct capitalization
        if data['transaction_category'] == TransactionCategory.STOCK and data.get('symbol'):
            data['symbol'] = data['symbol'].upper()
        if data['transaction_category'] == TransactionCategory.CRYPTO and data.get('name'):
            data['name'] = data['name'].lower()

        # Ensure presence of symbol for stocks and name for cryptos
        if data['transaction_category'] == TransactionCategory.STOCK and not data.get('symbol'):
            raise serializers.ValidationError("Stock symbol is required for stocks.")
        if data['transaction_category'] == TransactionCategory.CRYPTO and not data.get('name'):
            raise serializers.ValidationError("Crypto name is required for crypto.")

        # Validate cash balance for buy transactions
        if data['transaction_type'] == TransactionType.BUY:
            cash_balance = CashBalance.objects.get(user=user).balance
            total_cost = data['quantity'] * data['trade_price'] + data['commission']
            if total_cost > cash_balance:
                raise serializers.ValidationError(
                    {'cash_balance': _('Insufficient cash balance for this transaction.')})

        # Validate portfolio quantity for sell transactions
        if data['transaction_type'] == TransactionType.SELL:
            portfolio_entry = PortfolioEntry.objects.filter(
                user=user,
                investment_type=data['transaction_category'],
                investment_symbol=data['symbol'] if data['transaction_category'] == TransactionCategory.STOCK else
                data['name']
            ).first()
            if not portfolio_entry:
                raise serializers.ValidationError(
                    {'portfolio_entry': _('You currently do not own this asset so it cannot be sold.')})
            if data['quantity'] > portfolio_entry.quantity:
                raise serializers.ValidationError({'quantity': _('Cannot sell more than the available quantity.')})

        return data


class CashTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashTransaction
        exclude = ('user',)

    def validate(self, data):
        user = self.context['request'].user

        # Validate that for withdrawal transactions, the cash balance is sufficient.
        if data['transaction_type'] == CurrencyTransactionType.CASH_WITHDRAWAL:
            cash_balance = CashBalance.objects.get(user=user).balance
            if data['amount'] + data['commission'] > cash_balance:
                raise serializers.ValidationError(
                    {'cash_balance': _('Insufficient cash balance for this transaction.')})
        return data


class PortfolioEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEntry
        fields = '__all__'
        read_only_fields = ('user', 'investment_type', 'investment_symbol', 'investment_name', 'quantity',
                            'average_trade_price', 'commissions', 'cost_basis', 'current_price', 'current_value',
                            'profit_loss', 'profit_loss_percent')


class CashBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBalance
        fields = '__all__'
