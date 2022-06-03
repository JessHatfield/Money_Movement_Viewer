from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea


class MoneyMovementNote(FlaskForm):
    user_note = StringField('User Note',widget=TextArea())
    submit = SubmitField('Submit')
