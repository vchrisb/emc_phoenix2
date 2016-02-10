#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "------ delete database tables ------"
python $DIR/wipe_psql_database.py --force

echo "------ delete all keys in bucket ------"
python $DIR/wipe_bucket.py --force

echo "------ create database tables ------"
python manage.py migrate --noinput

echo "------ create default superuser ------"
python $DIR/superuser.py

echo "------ starting waitress  ------"
waitress-serve --port=$PORT phoenix.wsgi:application
