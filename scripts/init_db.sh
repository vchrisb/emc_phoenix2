#!/bin/sh
echo "------ Create database tables ------"
python manage.py migrate --noinput

echo "------ create default admin user ------"
python scripts/superuser.py

echo "------ starting waitress  ------"
waitress-serve --port=$PORT phoenix.wsgi:application
