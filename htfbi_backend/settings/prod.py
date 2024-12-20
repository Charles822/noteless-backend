from .common import *
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = ['noteless-prod-8f2da775e481.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True) # changed to postgres
}

# CORS_ALLOWED_ORIGINS = [
#     'https://noteless-prod-k03g37a3e-charles-fauchets-projects.vercel.app',
# ]

CORS_ALLOW_ALL_ORIGINS = True

REDIS_URL = os.environ['REDIS_URL']

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# can use the same REDIS url for caching later.

SITE_URL = 'https://www.noteless.xyz/checkout'