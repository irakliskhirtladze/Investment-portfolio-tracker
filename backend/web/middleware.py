import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_token = request.COOKIES.get('access_token')
        if auth_token:
            try:
                token = AccessToken(auth_token)
                user_id = token['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
            except jwt.ExpiredSignatureError:
                pass
            except jwt.DecodeError:
                pass
            except User.DoesNotExist:
                pass
