from rest_framework import generics, permissions
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta

from stats.models import PortfolioValue
from stats.serializers import PortfolioStatsSerializer, PortfolioValueSerializer


class PortfolioStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        today = timezone.now().date()

        # Fetch the latest portfolio values
        end_of_day = PortfolioValue.objects.filter(user=user, date=today).last()
        end_of_week = PortfolioValue.objects.filter(user=user, date__gte=today - timedelta(days=7)).last()
        end_of_month = PortfolioValue.objects.filter(user=user, date__gte=today - timedelta(days=30)).last()

        # Calculate the cushion
        if end_of_day:
            investments_value = end_of_day.investments_value
            total_value = end_of_day.total_value
            cushion = (investments_value / total_value) * 100 if total_value != 0 else 0
        else:
            cushion = 0

        # Prepare the response data
        data = {
            'end_of_day': PortfolioValueSerializer(end_of_day).data if end_of_day else None,
            'end_of_week': PortfolioValueSerializer(end_of_week).data if end_of_week else None,
            'end_of_month': PortfolioValueSerializer(end_of_month).data if end_of_month else None,
            'cushion': cushion
        }

        return Response(data)

