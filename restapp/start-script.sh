#! /bin/bash

until nc -v -z -w 5 db 3306
do
	echo 'Waiting for db...'
	sleep 5
done
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
