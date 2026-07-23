#!/bin/bash

set -o errexit

pip install -r requirements.txt

cd doctor
python manage.py collectstatic --no-input
python manage.py migrate
