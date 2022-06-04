
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

* Edit user notes per money_movement.

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