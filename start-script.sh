#! /bin/bash

# Check if it's production with DB (NODB is empty) or local deploy (not empty, any text)
echo "NODB = $NODB"
if [ -z $NODB ]
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
