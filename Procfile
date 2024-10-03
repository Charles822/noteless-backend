release: python manage.py migrate
web: gunicorn htfbi_backend.wsgi
worker: celery -A htfbi_backend worker