# Start API server
pip install -r requirements2.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver