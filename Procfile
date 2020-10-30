release: python3 manage.py migrate
celery: celery -A ama worker -l info
web: gunicorn ama.wsgi