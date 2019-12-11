#!/bin/sh
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm -f db.sqlite3

# Create tables

python manage.py makemigrations
python manage.py createcachetable
python manage.py migrate

# Load init data to db

python manage.py loaddata init_data/orderstatus.json
python manage.py loaddata init_data/cities.json
python manage.py loaddata init_data/orderrespondstatus.json
python manage.py loaddata init_data/categories.json
python manage.py loaddata init_data/subcategories.json
python manage.py loaddata init_data/orderlocationtype.json
python manage.py loaddata init_data/payments.json
python manage.py loaddata init_data/languages.json