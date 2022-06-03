from app.routes import bp
# allows us to log messages via the logger instance attached to global app
from flask import current_app, render_template
from app.models import MoneyMovement


# In production Nginx would capture URL/IP/Method
# Flask logs should concern themselves with the application specific information within request and it's processing


@bp.route('/')
def view_all_money_movements():
    money_movements = MoneyMovement.query.all()

    current_app.logger.info("This Is A Logging Test")

    return render_template("view_money_movements.html", money_movements=money_movements)


@bp.route('/view_money_movement/<movement_id>')
def view_single_money_movement(movement_id):
    # return 404 if id does not exist

    # else return the template
    money_movement = MoneyMovement.query.filter_by(id=movement_id).first()

    return render_template("edit_money_movement.html", money_movement=money_movement)
    pass
