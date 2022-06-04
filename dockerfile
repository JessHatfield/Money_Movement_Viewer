FROM ubuntu:20.04


#docker sees current working directory as "Money_Movement_Viewer/docker_deployment"

#Copy across application files
copy /app /money_movement_viewer_app/app
copy webapp.py /money_movement_viewer_app/webapp.py
copy setup_db.py /money_movement_viewer_app/setup_db.py
copy /docker_deployment/start_app.sh /money_movement_viewer_app/start_app.sh

#Use production dotfile
add /docker_deployment/.prod_env /money_movement_viewer_app/app/.env

#Setup Python
run apt-get update && apt-get install -y
run apt install -y python3-pip
run apt install -y python3.8-distutils

#WORKDIR exists within the container
WORKDIR "/money_movement_viewer_app"

#Install requirements
run pip install -r /money_movement_viewer_app/app/requirements.txt

#Launch Application
env FLASK_ENV production

expose 5000
cmd ["bash","/money_movement_viewer_app/start_app.sh"]








