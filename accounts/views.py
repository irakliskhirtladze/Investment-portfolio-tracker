from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import requests


class ActivateUser(GenericAPIView):
    def get(self, request, uid, token, format = None):
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/api/v1/auth/users/activation/"
        response = requests.post(url, data = payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())
