from rest_framework import serializers
from stats.models import PortfolioValue


class PortfolioValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioValue
        fields = '__all__'
