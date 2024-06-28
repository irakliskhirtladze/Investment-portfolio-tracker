from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from portfolio.models import InvestmentTransaction, CashTransaction
from portfolio.serializers import InvestmentTransactionSerializer, CashTransactionSerializer


class InvestmentTransactionViewSet(viewsets.ModelViewSet):
    queryset = InvestmentTransaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestmentTransactionSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            # Add user to serializer data
            serializer.save(user=self.request.user)
        except DjangoValidationError as e:
            # Catch model validation errors and raise DRF validation errors
            raise DRFValidationError(e.message_dict)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except DRFValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CashTransactionViewSet(viewsets.ModelViewSet):
    queryset = CashTransaction.objects.all()
    serializer_class = CashTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
