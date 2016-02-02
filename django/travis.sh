#!/bin/sh
echo "------ delete database tables ------"
python manage.py sqlflush | python manage.py dbshell

echo "------ create database tables ------"
python manage.py migrate --noinput

echo "------ create default admin user ------"
python manage.py shell < superuser.py

echo "------ starting gunicorn  ------"
waitress-serve --port=$PORT phoenix.wsgi:application