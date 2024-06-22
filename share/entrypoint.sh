#!/bin/sh

# Wait for PostgreSQL to be ready
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Apply database migrations
echo "Apply database migrations"
pipenv run python manage.py migrate

# Collect static files
echo "Collect static files"
pipenv run python manage.py collectstatic --noinput

exec pipenv run "$@"




