#!/bin/bash

yes | ssh-keygen -f /root/.ssh/id_rsa -t rsa -N '' &&
python manage.py collectstatic --noinput && 
gunicorn config.wsgi -b 0.0.0.0:8000 --workers=3 --threads 2 --reload