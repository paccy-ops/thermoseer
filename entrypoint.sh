#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py migrate

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"school@gmail.com"}
python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
python manage.py migrate

exec "$@"