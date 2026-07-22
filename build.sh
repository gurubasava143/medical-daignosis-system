#!/bin/bash

set -o errexit

pip install -r requirements.txt

python doctor/manage.py collectstatic --no-input

python doctor/manage.py migrate
