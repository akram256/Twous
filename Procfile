release: python manage.py makemigrations
release: python manage.py migrate
celery: celery -A backend_towus worker -l info
web: gunicorn ama.wsgi