from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'htfbi_backend.settings.dev')

app = Celery('htfbi_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    }
)

app.autodiscover_tasks()