#!/bin/bash

echo '========== MAKING MIGRATIONS'
python manage.py makemigrations

echo '========== RUNNING MIGRATIONS'
python manage.py migrate

echo '========== RUNNING SERVER'
python manage.py runserver 0.0.0.0:$PORT
