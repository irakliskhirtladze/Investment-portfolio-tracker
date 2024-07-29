from rest_framework import serializers
from stats.models import PortfolioValue

class PortfolioValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioValue
        fields = '__all__'


class PortfolioStatsSerializer(serializers.Serializer):
    end_of_day = PortfolioValueSerializer()
    end_of_week = PortfolioValueSerializer()
    end_of_month = PortfolioValueSerializer()
    cushion = serializers.DecimalField(max_digits=5, decimal_places=2)
