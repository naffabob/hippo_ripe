from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PrefixForm(FlaskForm):
    prefix = StringField('Префикс', validators=[DataRequired()])
    submit = SubmitField('Save')
