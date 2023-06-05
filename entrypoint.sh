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

SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"school"}
python manage.py createsuperuser --username $SUPERUSER_USERNAME --noinput || true

exec "$@"