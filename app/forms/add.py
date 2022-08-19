from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class Add(FlaskForm):
    front = StringField('Front')
    back = StringField('Back')
    submit = SubmitField('Submit')
