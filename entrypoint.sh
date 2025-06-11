#!/bin/bash

set -e  # Stop on error

cd EBoutique_API

echo "🛠 Running migrations..."
python3 manage.py migrate

echo "🚀 Starting development server on 0.0.0.0:${PORT:-5000} ..."
exec python3 manage.py runserver 0.0.0.0:${PORT:-5000}
