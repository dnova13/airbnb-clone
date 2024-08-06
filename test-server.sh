#!/bin/bash

# python -m venv /app/myvenv
cd /app/airbnb-clone
source /app/myvenv/bin/activate
python manage.py test --settings='config.test_settings'
