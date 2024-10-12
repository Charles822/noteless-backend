release: python manage.py migrate
web: gunicorn htfbi_backend.wsgi --config htfbi_backend/gunicorn.conf.py --bind 0.0.0.0:$PORT
worker: celery -A htfbi_backend worker --loglevel=debug