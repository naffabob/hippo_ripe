from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClientForm(FlaskForm):
    name = StringField('Название клиента', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={"class": "btn btn-primary"})
