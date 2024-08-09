from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import requests


class MockUser:
    """A mock user object to represent authenticated users."""
    def __init__(self, id, email, name, is_authenticated=True):
        self.id = id
        self.email = email
        self.name = name
        self.is_authenticated = is_authenticated

    def __str__(self):
        return self.email


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            request.user = AnonymousUser()
            return

        try:
            # Verify token by calling the API
            headers = {'Authorization': f'Bearer {auth_token}'}
            response = requests.get(f"{settings.API_BASE_URL}/auth/users/me/", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()

                # Use a mock user object to represent the authenticated user
                user = MockUser(
                    id=user_data.get('id'),
                    email=user_data.get('email'),
                    name=user_data.get('name', '')
                )

                request.user = user
            else:
                request.user = AnonymousUser()
        except Exception as e:
            # Log the exception if needed
            request.user = AnonymousUser()

    def process_response(self, request, response):
        return response
