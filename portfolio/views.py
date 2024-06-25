from portfolio.models import Portfolio
from rest_framework import viewsets
from rest_framework.response import Response


class PortfolioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Portfolio.objects.all()
    serializer_class = Portfolio
