#!/bin/bash

python manage.py flush --noinput
git pull origin master

python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py add_bike_data