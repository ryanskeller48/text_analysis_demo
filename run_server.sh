# Start API server
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py migrate --run-syncdb
python3 manage.py runserver
