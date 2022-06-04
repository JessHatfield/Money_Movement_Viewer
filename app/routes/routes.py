from flask_login import login_required, current_user

from app.forms import MoneyMovementNoteForm
from app.routes import bp
# allows us to log messages via the logger instance attached to global app
from flask import current_app, render_template, flash
from app.models import MoneyMovement
from app.extensions import db


# In production Nginx would capture URL/IP/Method
# Flask logs should concern themselves with the application specific information within request, and it's processing
# Logs with the level of info are messages designed to be easily read by humans and give a short description of the action which as happened
# Logs with the level of debug are designed to be easily read by machines. These are json which can then be parsed by a log viewer. They contain more specifics on the data structures being worked on
# The "message" key within debug message must the same for each instance of the log message to be easily searchable. For example "Login Successful" vs "<User 1> Has Successfully Logged In"
# When debugging we can use info level messages to follow the flow of execution and then drop into debug level when we need more specifics (for example when trying to re-create or stimulate a bug).


@bp.route('/')
@login_required
def view_all_money_movements():
    money_movements = MoneyMovement.query.all()

    current_app.logger.info(f"Returning Money Movements For {current_user}")
    return render_template("view_money_movements.html", money_movements=money_movements)


@bp.route('/view_money_movement/<movement_id>', methods=['POST'])
@login_required
def edit_money_movement_note(movement_id):
    user_note_form = MoneyMovementNoteForm()

    if user_note_form.validate_on_submit():
        new_user_note = user_note_form.data['user_note']

        money_movement = MoneyMovement.query.filter_by(id=movement_id).first()

        money_movement.user_note = new_user_note

        db.session.commit()

        current_app.logger.info(f"Updated Note For {money_movement} For {current_user}")
        current_app.logger.debug({"message": "Updated Note For Money Movement", "money_movement": money_movement,
                                  "user_note": new_user_note, "user": current_user})

        flash("User Note Updated Successfully")

        return render_template("edit_money_movement.html", money_movement=money_movement, form=user_note_form)


@bp.route('/view_money_movement/<movement_id>', methods=['GET'])
@login_required
def view_single_money_movement(movement_id):
    user_note_form = MoneyMovementNoteForm()
    money_movement = MoneyMovement.query.filter_by(id=movement_id).first()

    current_app.logger.info(f"Returning {money_movement} For {current_user}")
    return render_template("edit_money_movement.html", money_movement=money_movement, form=user_note_form)
