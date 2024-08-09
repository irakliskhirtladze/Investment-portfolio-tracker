from config.settings.base import *


SECRET_KEY = "django-insecure-2^_51&^6xv=&f^$pkkgtlc4=kkp)s9ne9jpfy=c6bd#7^i&abs"

DEBUG = True

FINNHUB_API_KEY = "cqmr481r01qjs6oce1ugcqmr481r01qjs6oce1v0"

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SITE_DOMAIN = "localhost:8000"
SITE_NAME = "Portfolio Tracker"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "portfolio_tracker",
        'USER': 'dev',
        'PASSWORD': 'devpass',
        'HOST': 'db',
        'PORT': '5432',
    }
}

API_BASE_URL = 'http://127.0.0.1:8000/api'

CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://localhost:8000']


# Celery settings
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Email settings
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
if EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
