#!/bin/bash

set -e  # Stop on error

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🛠 Running migrations..."
python manage.py migrate --noinput

echo "🚀 Starting development server on 0.0.0.0:8000 ..."
exec python manage.py runserver 0.0.0.0:8000