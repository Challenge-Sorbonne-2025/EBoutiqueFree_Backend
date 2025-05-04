#!/bin/bash

set -e  # Stop on error

echo "📦 Collecting static files..."
python EBoutique_API/manage.py collectstatic --noinput

echo "🛠 Running migrations..."
python EBoutique_API/manage.py migrate --noinput

echo "🚀 Starting development server on 0.0.0.0:8000 ..."
exec python EBoutique_API/manage.py runserver 0.0.0.0:8000