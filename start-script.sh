#! /bin/bash

until nc -v -z -w 5 db 3306
do
	echo 'Waiting for db...'
	sleep 5
done
python restapp/manage.py makemigrations
python restapp/manage.py migrate
python restapp/manage.py runserver 0.0.0.0:8000
