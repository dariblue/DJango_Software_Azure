#!/bin/bash
set -e

echo "=== Arrancando aplicación ReleCloud Django ==="

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Cargando datos iniciales (Station-9101460 y cruceros)..."
python manage.py seed_data

echo "Iniciando servidor Gunicorn..."
gunicorn --bind=0.0.0.0 --timeout 600 project.wsgi
