from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea


class MoneyMovementNoteForm(FlaskForm):
    user_note = StringField('Edit User Note',widget=TextArea())
    submit = SubmitField('Submit')
