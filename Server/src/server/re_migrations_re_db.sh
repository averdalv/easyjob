#!/bin/sh
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm -f db.sqlite3

# Create tables

python3 manage.py makemigrations
python3 manage.py createcachetable
python3 manage.py migrate

# Load init data to db

python3 manage.py loaddata init_data/orderstatus.json
python3 manage.py loaddata init_data/cities.json
python3 manage.py loaddata init_data/orderrespondstatus.json
python3 manage.py loaddata init_data/categories.json
python3 manage.py loaddata init_data/subcategories.json
python3 manage.py loaddata init_data/orderlocationtype.json
python3 manage.py loaddata init_data/payments.json
python3 manage.py loaddata init_data/languages.json