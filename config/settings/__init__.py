import os
from decouple import config

ENVIRONMENT = config('ENVIRONMENT', default='dev')

if ENVIRONMENT == 'prod':
    from .prod import *
elif ENVIRONMENT == 'dev':
    from .dev import *
