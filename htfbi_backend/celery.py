from __future__ import absolute_import, unicode_literals
import os, ssl
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'htfbi_backend.settings.dev')

app = Celery('htfbi_backend')

app.conf.update(
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    }
)

# app.conf.broker_connection_retry_on_startup = True # silence warning: broker connection retries are made during startup

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()