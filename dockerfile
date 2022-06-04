FROM ubuntu:20.04


copy . /Money_Movement_Viewer

#Use production dotfile
add .prod_env /Money_Movement_Viewer/.env

#Setup Python
run apt-get update && apt-get install -y
run apt install -y python3-pip
run apt install -y python3.8-distutils

WORKDIR "/Money_Movement_Viewer"

#Install requirements
run pip install -r requirements.txt

#Launch Application
env FLASK_ENV production

expose 5000
cmd ["bash","start_app.sh"]

#cmd ["gunicorn","--bind","0.0.0.0:5000","webapp:app"]






