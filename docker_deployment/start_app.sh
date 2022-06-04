echo "Create Tables Within Production DB"
ls -a
python3.8 setup_db.py
echo "Starting Webapp"
gunicorn -b 0.0.0.0:5000 webapp:app
