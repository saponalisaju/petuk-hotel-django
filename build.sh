#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
python manage.py collectstatic --noinput
python manage.py migrate --noinput
