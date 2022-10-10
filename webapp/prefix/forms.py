from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PrefixForm(FlaskForm):
    prefix = StringField('Префикс', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={"class": "btn btn-primary"})
