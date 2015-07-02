#!/bin/sh
cd /code
python manage.py syncdb --noinput
python manage.py loaddata init-data.json
python manage.py runserver 0.0.0.0:8000
