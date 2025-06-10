#!/bin/bash

set -e  # Stop on error

pwd
cd EBoutique_API
pwd

#echo "📦 Collecting static files..."
#python3 manage.py collectstatic --noinput

echo "🛠 Running migrations..."
python3 manage.py migrate #--noinput

echo "🚀 Starting development server on 0.0.0.0:5000:5000 ..."
exec python3 manage.py runserver 0.0.0.0:5000:5000
