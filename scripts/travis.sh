#!/bin/sh
echo "------ delete database tables ------"
python wipe_psql_database.py --force

echo "------ delete all keys in bucket ------"
python wipe_bucket.py --force

echo "------ create database tables ------"
python manage.py migrate --noinput

echo "------ create default superuser ------"
python superuser.py

echo "------ starting waitress  ------"
waitress-serve --port=$PORT phoenix.wsgi:application
