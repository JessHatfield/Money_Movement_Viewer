echo "Create Tables Within Production DB"
python3.8 setup_db.py

gunicorn -b 0.0.0.0:5000 webapp:app
