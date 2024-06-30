from rest_framework import serializers

from portfolio.models import InvestmentTransaction, CashTransaction, PortfolioEntry, CashBalance


class CashBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBalance
        fields = ['balance']


class InitialPortfolioEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEntry
        fields = ['investment_type', 'investment_symbol', 'investment_name', 'quantity', 'average_trade_price']


class PortfolioEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEntry
        fields = '__all__'


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


class CashBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBalance
        fields = '__all__'
