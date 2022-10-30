from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp


class ClientForm(FlaskForm):
    render_kw = {"class": "form-control"}
    name = StringField('Client name', validators=[DataRequired()], render_kw=render_kw)


class ClentPeerForm(FlaskForm):
    min_string_value = 5
    max_string_value = 13
    asn = StringField(
        validators=[
            DataRequired(message='The field is required'),
            Length(
                min=min_string_value,
                max=max_string_value,
                message=f'From {min_string_value} to {max_string_value} characters'
            ),
            Regexp(regex='^AS[0-9]*$', message='Wrong ASN format [AS999]'),
        ],
        render_kw={'class': 'form-control', 'placeholder': 'ASN'},
    )
    asset = StringField(render_kw={'class': 'form-control', 'placeholder': 'ASSET'})
    remark = StringField(render_kw={'class': 'form-control', 'placeholder': 'Remark'})
