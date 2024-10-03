from .common import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['noteless-prod-8f2da775e481.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}


REDIS_URL = os.environ['REDIS_URL']

CELERY_BROKER_URL = 'REDIS_URL'
CELERY_RESULT_BACKEND = 'REDIS_URL'

# can use the same REDIS url for caching later.