#!/bin/sh
echo "------ Create database tables ------"
python manage.py migrate --noinput

echo "------ starting waitress  ------"
waitress-serve --port=$PORT phoenix.wsgi:application
