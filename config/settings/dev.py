from config.settings.base import *
from decouple import config, Csv

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

FINNHUB_API_KEY = config('FINNHUB_API_KEY')

SECRET_KEY = "django-insecure-2^_51&^6xv=&f^$pkkgtlc4=kkp)s9ne9jpfy=c6bd#7^i&abs"

SITE_DOMAIN= "localhost:8000"
SITE_NAME= "Portfolio Tracker"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

API_BASE_URL = 'http://127.0.0.1:8000/api'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', 'db'),
        'PORT': config('DB_PORT', '5432'),
    }
}

CORS_ALLOWED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

# Celery settings
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
