#!/bin/sh

# Prepare log files and start outputting logs to stdout
touch /logs/gunicorn.log
touch /logs/gunicorn-access.log

export DJANGO_SETTINGS_MODULE=jamf_webhook_connector.settings

./wait-for-it.sh db:5432 -s -t 60 -- echo 'Database is up'
python jamf_webhook_connector/manage.py migrate
python jamf_webhook_connector/manage.py makemigrations
python jamf_webhook_connector/manage.py migrate
python jamf_webhook_connector/manage.py collectstatic --no-input
cd jamf_webhook_connector
#gunicorn jamf_webhook_connector.wsgi:application --bind 0.0.0.0:8000

exec gunicorn jamf_webhook_connector.wsgi:application \
    --name jamfhooks \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
    --access-logfile=/logs/gunicorn-access.log
  "$@"
