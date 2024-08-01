import requests
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings


class ActivateUser(APIView):
    """
    View to activate users automatically after following the activation link sent to their email.
    """
    permission_classes = [AllowAny]

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}
        url = f"{settings.API_BASE_URL}/auth/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({"message": "Your account has been activated!"}, status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)
