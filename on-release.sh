python manage.py collectstatic --noinput --clear && gunicorn config.wsgi
