from flask import Blueprint

bp = Blueprint('money_movement', __name__)

from app.money_movements import routes