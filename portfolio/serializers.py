from rest_framework import serializers

from portfolio.models import InvestmentTransaction, CashTransaction, PortfolioEntry, CashBalance


class InitialCashBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBalance
        fields = ['balance']


class InitialPortfolioEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEntry
        fields = ['investment_type', 'investment_symbol', 'investment_name', 'quantity', 'average_trade_price']


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentTransaction
        exclude = ('user',)


class CashTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashTransaction
        exclude = ('user',)


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
