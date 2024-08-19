from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from portfolio.models import InvestmentTransaction, CashTransaction, CashBalance, PortfolioEntry
from portfolio.serializers import InvestmentTransactionSerializer, CashTransactionSerializer, \
    InitialPortfolioEntrySerializer, CashBalanceSerializer, PortfolioEntrySerializer, \
    CombinedPortfolioSerializer, CashBalanceSerializer, EmptySerializer
from portfolio.utils import calculate_portfolio_entry_fields, refresh_portfolio, update_portfolio_entry, \
    update_cash_balance


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to view their portfolio entries and refresh the portfolio.
    """
    queryset = PortfolioEntry.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioEntrySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def total_portfolio_value(self, user):
        """Returns the total value of the portfolio. Cash balance + current values of portfolio entries"""
        cash_balance = CashBalance.objects.filter(user=self.request.user).first()
        portfolio_entries = self.get_queryset()
        total_value = cash_balance.balance if cash_balance else 0
        for entry in portfolio_entries:
            total_value += entry.current_value
        return total_value

    def list(self, request, *args, **kwargs):
        """Returns the cash balance and portfolio entries for the authenticated user."""
        user = request.user
        cash_balance = CashBalance.objects.filter(user=user).first() or 0
        portfolio_entries = self.get_queryset()

        combined_data = {
            'total_portfolio_value': self.total_portfolio_value(user),
            'cash_balance': cash_balance,
            'portfolio_entries': PortfolioEntrySerializer(portfolio_entries, many=True).data
        }

        serializer = CombinedPortfolioSerializer(combined_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='refresh', serializer_class=EmptySerializer)
    def refresh_portfolio(self, request):
        """
        Refreshes the portfolio entries by updating the current prices and recalculating dependent fields.
        """
        refresh_portfolio(request.user)
        return Response({"detail": "Portfolio refreshed successfully."}, status=status.HTTP_200_OK)


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
        InvestmentTransaction.objects.filter(user=user).delete()
        CashTransaction.objects.filter(user=user).delete()

        # Handle cash balance
        cash_data = request.data.get('cash_balance')
        if cash_data:
            cash_data['user'] = user.id
        cash_serializer = CashBalanceSerializer(data=cash_data)
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
                    try:
                        portfolio_entry, created = PortfolioEntry.objects.update_or_create(
                            user=user,
                            asset_type=entry_serializer.validated_data['asset_type'],
                            asset_symbol=entry_serializer.validated_data['asset_symbol'],
                            defaults=entry_serializer.validated_data
                        )
                        calculate_portfolio_entry_fields(portfolio_entry)
                        portfolio_entry.save()
                    except ValidationError as e:
                        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(entry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Initial setup completed successfully."}, status=status.HTTP_201_CREATED)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or create transactions once initial setup is complete.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = InvestmentTransaction.objects.all()
    serializer_class = InvestmentTransactionSerializer

    def get_serializer_class(self):
        if self.action in ['create_investment_transaction', 'list_investment_transactions']:
            return InvestmentTransactionSerializer
        if self.action in ['create_cash_transaction', 'list_cash_transactions']:
            return CashTransactionSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        if isinstance(transaction, InvestmentTransaction):
            update_portfolio_entry(self.request.user, transaction)
        update_cash_balance(self.request.user, transaction)

    @action(detail=False, methods=['post'], url_path='create-investment-transaction')
    def create_investment_transaction(self, request, *args, **kwargs):
        return self.handle_creation(request)

    @action(detail=False, methods=['post'], url_path='create-cash-transaction')
    def create_cash_transaction(self, request, *args, **kwargs):
        return self.handle_creation(request)

    @action(detail=False, methods=['get'], url_path='list-investment-transactions')
    def list_investment_transactions(self, request, *args, **kwargs):
        queryset = InvestmentTransaction.objects.filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list-cash-transactions')
    def list_cash_transactions(self, request, *args, **kwargs):
        queryset = CashTransaction.objects.filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def handle_creation(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BalanceUpdateView(APIView):
    """
    Allows users to update the cash balance by posting a single number.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CashBalanceSerializer(data=request.data)
        if serializer.is_valid():
            balance = serializer.validated_data['balance']
            CashBalance.objects.update_or_create(
                user=request.user, defaults={'balance': balance}
            )
            return Response({"detail": "Cash balance updated successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
