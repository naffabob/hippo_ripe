from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PeerForm(FlaskForm):
    asn = StringField('Номер AS', validators=[DataRequired()])
    asset = StringField('AS-SET')
    client = StringField('Название клиента')
    submit = SubmitField('Save')


class PrefixForm(FlaskForm):
    prefix = StringField('Префикс', validators=[DataRequired()])
    submit = SubmitField('Save')
