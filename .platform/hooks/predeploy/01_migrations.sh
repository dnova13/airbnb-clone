#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging

python manage.py migrate
# daphne -b 0.0.0.0 -p 8452 config.asgi:application