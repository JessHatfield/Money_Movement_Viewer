from flask_login import login_required

from app.forms import MoneyMovementNote
from app.routes import bp
# allows us to log messages via the logger instance attached to global app
from flask import current_app, render_template, flash
from app.models import MoneyMovement
from app.extensions import db


# In production Nginx would capture URL/IP/Method
# Flask logs should concern themselves with the application specific information within request and it's processing


@bp.route('/')
@login_required
def view_all_money_movements():
    money_movements = MoneyMovement.query.all()
    return render_template("view_money_movements.html", money_movements=money_movements)


@bp.route('/view_money_movement/<movement_id>', methods=['POST'])
@login_required
def edit_money_movement_note(movement_id):
    user_note_form = MoneyMovementNote()

    if user_note_form.validate_on_submit():
        new_user_note = user_note_form.data['user_note']
        current_app.logger.info("Received New Note From User")

        money_movement = MoneyMovement.query.filter_by(id=movement_id).first()

        money_movement.user_note = new_user_note

        db.session.commit()

        current_app.logger.info(f"Updated Note For Money Transfer {money_movement}")
        current_app.logger.debug({"message": "Updated Note For Money Transfer", "money_movement": money_movement,
                                  "user_note": new_user_note})

        flash('User Note Updated Successfully')

        # Need to flash success message to user!

        return render_template("edit_money_movement.html", money_movement=money_movement, form=user_note_form)


@bp.route('/view_money_movement/<movement_id>', methods=['GET'])
@login_required
def view_single_money_movement(movement_id):
    # return 404 if id does not exist

    # else return the template
    user_note_form = MoneyMovementNote()
    money_movement = MoneyMovement.query.filter_by(id=movement_id).first()

    return render_template("edit_money_movement.html", money_movement=money_movement, form=user_note_form)

