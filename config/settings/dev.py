# config/settings/development.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

API_BASE_URL = 'http://127.0.0.1:8000'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
