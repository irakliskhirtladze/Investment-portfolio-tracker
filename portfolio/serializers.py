from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from portfolio.choices import TransactionType, AssetType, CurrencyTransactionType
from portfolio.models import InvestmentTransaction, CashTransaction, PortfolioEntry, CashBalance
from portfolio.utils import fetch_stock_details, fetch_crypto_details


class CashBalanceSerializer(serializers.ModelSerializer):
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
        fields = ['asset_type', 'asset_symbol', 'quantity', 'average_trade_price']

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if data['average_trade_price'] <= 0:
            raise serializers.ValidationError("Average trade price must be greater than 0.")
        if data['asset_type'] == AssetType.STOCK and not data.get('asset_symbol'):
            raise serializers.ValidationError("Stock symbol is required for stocks.")
        if data['asset_type'] == AssetType.CRYPTO and not data.get('asset_symbol'):
            raise serializers.ValidationError("Crypto symbol is required for crypto.")

        # Fetch and populate name and price
        if data['asset_type'] == AssetType.STOCK:
            data['asset_symbol'] = data['asset_symbol'].upper()
            details = fetch_stock_details(data['asset_symbol'])
        elif data['asset_type'] == AssetType.CRYPTO:
            data['asset_symbol'] = data['asset_symbol'].lower()
            details = fetch_crypto_details(data['asset_symbol'])

        data['asset_name'] = details['name']
        data['current_price'] = details['price']

        return data


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentTransaction
        exclude = ('user',)

    def validate(self, data):
        user = self.context['request'].user

        # Ensure correct capitalization
        if data['asset_type'] == AssetType.STOCK and data.get('symbol'):
            data['symbol'] = data['symbol'].upper()
        if data['asset_type'] == AssetType.CRYPTO and data.get('symbol'):
            data['symbol'] = data['symbol'].lower()

        # Ensure presence of symbol for stocks and name for cryptos
        if data['asset_type'] == AssetType.STOCK and not data.get('symbol'):
            raise serializers.ValidationError("Stock symbol is required for stocks.")
        if data['asset_type'] == AssetType.CRYPTO and not data.get('symbol'):
            raise serializers.ValidationError("Crypto symbol is required for crypto.")

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
                asset_type=data['asset_type'],
                asset_symbol=data['symbol']
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
        fields = ['asset_type', 'asset_symbol', 'asset_name', 'quantity', 'average_trade_price', 'commissions',
                  'cost_basis', 'current_price', 'current_value', 'profit_loss', 'profit_loss_percent']


class CombinedPortfolioSerializer(serializers.Serializer):
    total_portfolio_value = serializers.DecimalField(max_digits=20, decimal_places=2)
    cash_balance = CashBalanceSerializer()
    portfolio_entries = PortfolioEntrySerializer(many=True)


class EmptySerializer(serializers.Serializer):
    pass
