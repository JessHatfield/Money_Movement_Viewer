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
sudo docker compose build
```

Run the Flask app and MySQL database containers using docker-compose.

```bash
sudo docker compose up

------------------------------------------
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [10] [INFO] Starting gunicorn 20.1.0
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [10] [INFO] Listening at: http://0.0.0.0:5000 (10)
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [10] [INFO] Using worker: sync
money_movement_viewer-app-1  | [2022-06-04 14:35:30 +0000] [12] [INFO] Booting worker with pid: 12


```

The application can then be accessed at http://0.0.0.0:5000.

* A premade user account has been created and can be used to login.

* The username is "joshuahatfield.jh@gmail.com" and the password is "password".

## Developing Locally

This guide assumes you have already installed python 3.8 (or greater), pip + python3.8-venv.

We also assume you have installed MYSQL version 5.7 (or greater).

Clone the git repository (skip this step if you have already cloned it)

```bash
  git clone https://github.com/JoshHatfield/Money_Movement_Viewer.git
```

Go to the project directory

```bash
  cd Money_Movement_Viewer
```

Create a new virtual environment

```bash
  sudo python3.8 -m venv ./money_movement_dev_env
```

Activate this new virtual environment

```bash
source ./money_movement_dev_env/bin/activate
```

Install project dependencies

```bash
sudo python3.8 -m pip install -r app/requirements.txt
```

Create Development + Test Databases

Enter the MySQL shell

```bash

sudo mysql


```

Create the development database

```bash
CREATE DATABASE money_movement_viewer_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Create the test database

```bash
CREATE DATABASE money_movement_viewer_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Create new database user

```bash

CREATE USER 'money_movement_viewer_admin'@'localhost' IDENTIFIED BY 'password';
```

Give this new user access to test and dev databases

```bash

GRANT ALL PRIVILEGES ON money_movement_viewer_dev.* TO 'money_movement_viewer_admin'@'localhost';
GRANT ALL PRIVILEGES ON money_movement_viewer_test.* TO 'money_movement_viewer_admin'@'localhost';
```

Create a .env file within the /app directory

```bash
sudo touch app/.env
```

Add the Database URI For The Development Database + a Secret Key for Flask-WTF CRSF protection to the .env file.

```bash
SQLALCHEMY_DATABASE_URI="mysql+pymysql://money_movement_viewer_admin:password@localhost:3306/money_movement_viewer_dev?charset=utf8mb4"
SECRET_KEY="This-Is-A-Secret-Key-For-Flask-CSRF"
```

Populate the development database with mocked data.

```bash
sudo python3.8 setup_db.py

-------------------------------------------------
Creating Tables Within Database
Creating Mock MoneyMovement Objects
Money Movement Objects Have Been Inserted Into Database
Creating User Account
User Object Has Been Inserted Into Database
```

Run Flask Integration Tests

```bash
sudo python3.8 -m unittest tests/test_routes.py


-------------------------------------------------
Ran 7 Tests in 6.5s

OK
```

```bash
sudo python3.8 -m unittest tests/test_models.py

-------------------------------------------------
Ran 4 Tests in 4s

OK

```

Start The Flask App

```bash
sudo python3.8 -m flask run
```

The application can be now accessed at http://127.0.0.1:5000

* A premade user account has been created and can be used to login.

* The username is "joshuahatfield.jh@gmail.com" and the password is "password".

## An Overview of Tech Choices Made



Why did we choose to build a Dynamic webapp vs a SPA?

* I normally build Single Page Applications using React + a Flask API, however (based on the feedback I had gotten) it
  seems that the Novus team prefer to build dynamic webapps.
* The application requirements where simple enough that they could be easily implemented using flask + jinja2.
* If the technical benefits are not great enough it makes most sense to build web-apps using the technology + approach
  used most frequently by the rest of the team.
* Therefore, choosing flask + jinja2 seemed like the most pragmatic option.

Why did I choose to use Flask-Login vs using a third party provider?

* I was hoping to implement a Google 0auth2 web flow as it would have offered a more frictionless ux and saved time in
  the long run if this where a production app. I've used auth0 in the past but was curious to see other free alternatives existed.
* A Google 0Auth2 have generated extra difficulties when it came to integration testing (mainly when it came to
  interacting with 0auth2 prompts offsite) and also required extra work to set up vs flask-login.
* Ultimately though, I only had a single day free for the app development and using flask-login was the most time efficient way of implementing the required features (login/logout/route protection).


Why did I use MYSQL?

* Users can potentially make simultaneous writes to the database however file based databases (
SQlIte) do not allow for concurrent writes? * I am most familiar with MySQL hence I chose to use it for this app. 
* Had there not been a requirement for concurrent writes I would have chosen SQlite as it is simpler to deploy via docker
and setup locally and offers similar read performance to MySQL.

## Additional Features Which Would Be Added With More Time

* Money Movement Search
    * Novus has 30,000 users. We can assume then that there are tens (or hundreds!) of thousands of money movements
      generated each month. Far too many to click through page by page.
    * Users of the money movement viewer would therefore benefit from being able to search through results for
      individual movements.
    * A basic search functionality could be implemented using SQL "LIKE" statements. An API based example can be
      [found here](https://github.com/JoshHatfield/Covid19-Research-Paper-Viewer/blob/e4d6c70784e9ee57dc4980fc88cf4108cec82a67/search_api/app/routes/routes.py#L41).
    * Users could then search for money movement using sender/receiver names or currency amounts.
    * A more advanced search could be achieved by moving to a pre-built search + analytics engine like Elasticsearch.
    * This could allow the user to construct more complex queries (for example show me all the movements over amount X
      for user Z between dates a + b).
    * This in turn would reduce the time to find key information whilst running audits. Enhancing the usability of the
      tool.

* "Last Modified Date" Pagination
    * Pagination is a core requirement when working with larger datasets. Failure to implement will lead to a noticeable
      slow down in site speeds when display hundreds or thousands of results.
    * Sorting money movements by last-modified date (most recent first) and splitting by date-ranges would be one
      method.
    * Using a last-modified date as opposed to an offset + limit prevents duplication caused by writes occurring between
      paginated results.
    * "Last-modified" date pagination also avoids slow-downs caused by SQL OFFSET commands as the database grows in
      size.

* Google 0Auth Login
    * Replacing the current login implementation with a third party identity provider (Google) would be worthwhile.
    * Implementing the ability to login with a pre-existing google account would come with the following benefits
        * Less friction for end user. They don't have to create a new set of login details (Novus staff all seem to use
          Google accounts).
        * Time saved vs having to implement password reset and 2FA (two key login features not currently implemented
          here!).
        * Reduce risk posed by a security breach as we no longer store user password hashes!