#!/bin/bash

set -e  # Stop on error

pwd
cd EBoutique_API
pwd

#echo "📦 Collecting static files..."
#python3 manage.py collectstatic --noinput

echo "🛠 Running migrations..."
python3 manage.py migrate #--noinput

echo "🚀 Starting development server on 127.0.0.0:8000 ..."
exec python3 manage.py runserver 127.0.0.0:8000
