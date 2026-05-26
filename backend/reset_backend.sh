#!/bin/bash

DB_NAME="testing_tools"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"

echo "==> Eliminando base de datos PostgreSQL..."
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -c "DROP DATABASE IF EXISTS $DB_NAME;"
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -c "CREATE DATABASE $DB_NAME;"

echo "==> Eliminando migraciones anteriores..."
rm -rf alembic/versions/*

echo "==> Generando migración inicial..."
alembic revision --autogenerate -m "initial schema"

echo "==> Aplicando migración..."
alembic upgrade head

echo "==> Ejecutando seed institucional..."
python backend/db/seed/seed_inicial.py

echo "==> TODO LISTO ✔"
