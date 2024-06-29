from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from portfolio.models import InvestmentTransaction, CashTransaction
from portfolio.serializers import InvestmentTransactionSerializer, CashTransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = InvestmentTransaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestmentTransactionSerializer

    def get_queryset(self, *args, **kwargs):
        if self.action in ['list_investment_transactions', 'create_investment_transaction']:
            return InvestmentTransaction.objects.filter(user=self.request.user)
        elif self.action in ['list_cash_transactions', 'create_cash_transaction']:
            return CashTransaction.objects.filter(user=self.request.user)
        return InvestmentTransaction.objects.none()

    def get_serializer_class(self):
        if self.action in ['create_investment_transaction', 'list_investment_transactions']:
            return InvestmentTransactionSerializer
        if self.action in ['create_cash_transaction', 'list_cash_transactions']:
            return CashTransactionSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        try:
            # Add user to serializer data
            serializer.save(user=self.request.user)
        except DjangoValidationError as e:
            # Catch model validation errors and raise DRF validation errors
            raise DRFValidationError(e.message_dict)

    def handle_creation(self, request):
        """
        Helper method that handles the creation of transactions for both investment and cash transactions
        to avoid code duplication.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except DRFValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='create-investment-transaction')
    def create_investment_transaction(self, request, *args, **kwargs):
        return self.handle_creation(request)

    @action(detail=False, methods=['post'], url_path='create-cash-transaction')
    def create_cash_transaction(self, request, *args, **kwargs):
        return self.handle_creation(request)

    @action(detail=False, methods=['get'], url_path='list-investment-transactions')
    def list_investment_transactions(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list-cash-transactions')
    def list_cash_transactions(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
