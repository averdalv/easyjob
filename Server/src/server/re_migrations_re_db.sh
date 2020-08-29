#!/bin/sh
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm -f db.sqlite3

python3 manage.py makemigrations authentication
python3 manage.py makemigrations customer
python3 manage.py makemigrations performer
python3 manage.py makemigrations gallery
python3 manage.py makemigrations order
python3 manage.py makemigrations location
python3 manage.py makemigrations chat
python3 manage.py makemigrations user_profile
python3 manage.py makemigrations verification
python3 manage.py createcachetable
python3 manage.py migrate

python3 manage.py shell -c "from authentication.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin')"
python3 manage.py loaddata init_data/users.json
python3 manage.py loaddata init_data/customers.json
python3 manage.py loaddata init_data/performers.json
python3 manage.py loaddata init_data/orderstatus.json
python3 manage.py loaddata init_data/cities.json
python3 manage.py loaddata init_data/orderrespondstatus.json
python3 manage.py loaddata init_data/categories.json
python3 manage.py loaddata init_data/subcategories.json
python3 manage.py loaddata init_data/orderlocationtype.json
python3 manage.py loaddata init_data/payments.json
python3 manage.py loaddata init_data/languages.json
python3 manage.py loaddata init_data/profiles.json
python3 manage.py loaddata init_data/locations.json
python3 manage.py loaddata init_data/orders.json