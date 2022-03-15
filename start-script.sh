#! /bin/bash

# Check if it's local deploy (not empty, any text) or production with DB
if [ -z $1 ]
then
	until nc -v -z -w 5 db 3306
	do
		echo 'Waiting for db...'
		sleep 5
	done
fi

hostname > /code/restapp/templates/api/base.html

python restapp/manage.py makemigrations
python restapp/manage.py migrate
python restapp/manage.py runserver 0.0.0.0:8000
