from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models.functions import TruncMonth, TruncDate
from stats.models import PortfolioValue
from stats.serializers import PortfolioValueSerializer


class PortfolioValueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view portfolio values.
    """
    queryset = PortfolioValue.objects.all()
    serializer_class = PortfolioValueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='daily/(?P<date>[^/.]+)')
    def daily(self, request, date=None):
        """
        Returns the portfolio values for a specific day.
        """
        date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        queryset = self.get_queryset().filter(timestamp__date=date_obj)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='monthly/(?P<month>[^/.]+)')
    def monthly(self, request, month=None):
        """
        Returns the portfolio values for a specific month.
        """
        month_obj = timezone.datetime.strptime(month, '%Y-%m').date()
        queryset = self.get_queryset().filter(timestamp__month=month_obj.month, timestamp__year=month_obj.year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='range')
    def date_range(self, request):
        """
        Returns the portfolio values for a specific date range.
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            start_date_obj = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = self.get_queryset().filter(timestamp__date__range=(start_date_obj, end_date_obj))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Please provide both start_date and end_date."}, status=400)

