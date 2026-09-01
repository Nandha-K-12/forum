#!/usr/bin/env bash
# Render build script for Django
set -o errexit

echo "=== Installing Dependencies ==="
pip install -r requirements.txt

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput

echo "=== Applying Database Migrations ==="
python manage.py migrate --noinput
