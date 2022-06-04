
# Money Movement Viewer

A small webapp for viewing money_movements between two people. Written using Flask + Jinja2.

#### Application Features

* View a list of money_movements detailing:
    * Last modified date for movement.
    * Money amount with ISO 4217 currency code.
    * Originating person.
    * Link to additional details page.

* View details for an individual money_movement detailing the above plus:
    * Receiving person.

* User can add notes per money_movement (and can use unicode characters).

* User Authentication
    * Pre-created user login + logout.
    * Un-authenticated users are redirected to login page when accessing protected routes.
    * Logged in users name is viewable within app.

* Deployment
    * Run via Gunicorn on Ubuntu 20.04 within docker container.
    * Log messages captured via sysout and via a rotating log file.

* Tests
    * Integration tests covering key happy paths for app routes.
    * Integration tests covering key behaviours for backend models.

#### Technology Used

* Flask/WTForms/Jinja2/Flask-Bootstrap for template creation + rendering.
* Flask-SQLalchemy + MySQL used for model creation + database.
* Flask-Login used for authentication.
* Unittest used for integration tests.
* Docker Compose + Gunicorn + Ubuntu 20.04 used for deployment.
## Getting Started

The application has been dockerised for ease of use

This guide assumes you have already installed docker + docker compose.


### Instructions

Clone the repository.

```bash
git clone https://github.com/JoshHatfield/Money_Movement_Viewer
```

Build the docker image containing the flask application.

```bash
cd Money_Movement_Viewer
docker compose build
```

Run the Flask app and MySQL database containers using docker-compose.

```bash
docker compose up

------------------------------------------
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [10] [INFO] Starting gunicorn 20.1.0
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [10] [INFO] Listening at: http://0.0.0.0:5000 (10)
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [10] [INFO] Using worker: sync
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [12] [INFO] Booting worker with pid: 12


```
The application can then be accessed at http://0.0.0.0:5000.

   * A premade user account has been created and can be used to login. 

   * The username is "joshuahatfield.jh@gmail.com" and the password is "password".



