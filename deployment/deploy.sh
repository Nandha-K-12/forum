#!/usr/bin/env bash
# Deployment automation script for Django Forum App
set -e

echo "=== Pulling latest changes ==="
git pull origin main

echo "=== Activating virtual environment ==="
source env/bin/activate

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Running database migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Restarting application via Supervisor ==="
sudo supervisorctl restart forum_app

echo "=== Deployment finished successfully! ==="
