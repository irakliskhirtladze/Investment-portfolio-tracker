from decimal import Decimal

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from portfolio.models import InvestmentTransaction, CashTransaction, CashBalance, PortfolioEntry
from portfolio.serializers import InvestmentTransactionSerializer, CashTransactionSerializer, \
    InitialPortfolioEntrySerializer, InitialCashBalanceSerializer, PortfolioEntrySerializer
from portfolio.utils import calculate_portfolio_entry_fields, refresh_portfolio


class InitialSetupView(APIView):
    """
    Helps user with initial setup of portfolio, with cash balance and portfolio entries.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        # Delete existing data (if any)
        CashBalance.objects.filter(user=user).delete()
        PortfolioEntry.objects.filter(user=user).delete()

        # Handle cash balance
        cash_data = request.data.get('cash_balance')
        if cash_data:
            cash_data['user'] = user.id
        cash_serializer = InitialCashBalanceSerializer(data=cash_data)
        if cash_serializer.is_valid():
            CashBalance.objects.update_or_create(user=user, defaults=cash_serializer.validated_data)
        else:
            return Response(cash_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle portfolio entries
        portfolio_data = request.data.get('portfolio_entries')
        if portfolio_data:
            for entry in portfolio_data:
                entry['user'] = user.id
                entry_serializer = InitialPortfolioEntrySerializer(data=entry)
                if entry_serializer.is_valid():
                    portfolio_entry, created = PortfolioEntry.objects.update_or_create(
                        user=user,
                        investment_type=entry_serializer.validated_data['investment_type'],
                        investment_symbol=entry_serializer.validated_data['investment_symbol'],
                        investment_name=entry_serializer.validated_data['investment_name'],
                        defaults=entry_serializer.validated_data
                    )
                    try:
                        portfolio_entry.full_clean()
                        portfolio_entry.save()
                    except DjangoValidationError as e:
                        return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(entry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Initial setup completed successfully."}, status=status.HTTP_200_OK)


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to view their portfolio entries and refresh the portfolio.
    """
    queryset = PortfolioEntry.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioEntrySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='refresh')
    def refresh_portfolio(self, request):
        """
        Refreshes the portfolio entries by updating the current prices and recalculating dependent fields.
        """
        user = request.user
        refresh_portfolio(user)
        return Response({"detail": "Portfolio refreshed successfully."}, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or create transactions once initial setup is complete.
    """
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
            # Create zero cash balance if it doesn't exist in DB
            CashBalance.objects.get_or_create(user=self.request.user)
            # Add user to serializer data
            serializer.save(user=self.request.user)
        except DjangoValidationError as e:
            # Catch model validation errors and raise DRF validation errors
            raise DRFValidationError(e.message_dict)

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

