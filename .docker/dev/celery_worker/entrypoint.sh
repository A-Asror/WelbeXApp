#!/bin/sh

# Install package
# pip install -r requirements/dev.txt

echo "DB Connection --- Establishing . . ."

# fast-api-postgresql this name of db, if the database name is called differently,set another name
while ! nc -z fast-api-postgresql 5432; do

    echo "DB Connection -- Failed!"

    sleep 1

    echo "DB Connection -- Retrying . . ."

done

echo "DB Connection --- Successfully Established!"

celery -A src.celery.settings worker -l info -S redbeat.RedBeatScheduler

exec "$@"
