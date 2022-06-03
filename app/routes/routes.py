
from app.routes import bp
# allows us to log messages via the logger instance attached to global app
from flask import current_app

# In production Nginx would capture URL/IP/Method
# Flask logs should concern themselves with the application specific information within request and it's processing


@bp.route('/')
def hello_world():

    current_app.logger.info("This Is A Logging Test")# put application's code here

    return 'Hello World!'
