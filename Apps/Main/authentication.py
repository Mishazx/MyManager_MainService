from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')
        print('api_key:', api_key)
        print('default_api_key:', settings.API_KEY)
        if not api_key or api_key != settings.API_KEY:
            raise AuthenticationFailed('Invalid or missing API Key')
        return (None, None)