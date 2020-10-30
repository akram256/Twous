release: python manage.py migrate
celery: celery -A backend_twous worker -l info
web: gunicorn backend_twous.wsgi