#!/bin/sh

# Wait for postgres to start
sleep 3

cd /app/src

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
# gunicorn aplazame.wsgi:application --bind 0.0.0.0:8000
