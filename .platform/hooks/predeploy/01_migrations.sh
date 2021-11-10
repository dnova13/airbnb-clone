#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging

python manage.py migrate
# python manage.py makemigrationspython manage.py compilemessages
# python manage.py createfirstsuperuser
# python manage.py collectstatic --noinput