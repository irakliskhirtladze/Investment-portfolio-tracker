from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth import get_user_model


class TestSetup(APITestCase):
    def setUp(self):
        self.portfolio_url = reverse('portfolio-list')
        self.portfolio_refresh_url = reverse('portfolio-refresh-portfolio')
        
        self.initial_setup_url = reverse('initial-setup')
        self.update_balance_url = reverse('update-balance')

        self.create_investment_transaction_url = reverse('transactions-create-investment-transaction')
        self.create_cash_transaction_url = reverse('transactions-create-cash-transaction')
        self.list_investment_transactions_url = reverse('transactions-list-investment-transactions')
        self.list_cash_transactions_url = reverse('transactions-list-cash-transactions')

        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }

        self.user = get_user_model().objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
