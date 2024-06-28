from rest_framework import serializers

from portfolio.models import InvestmentTransaction, CashTransaction


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentTransaction
        exclude = ('user',)


class CashTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashTransaction
        exclude = ('user',)
