import os

from dotenv import load_dotenv

# This gives us the root directory of the project
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))




class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
