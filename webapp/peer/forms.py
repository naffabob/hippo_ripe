from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp


class PeerForm(FlaskForm):
    min_string_value = 5
    max_string_value = 13
    asn = StringField(
        label='ASN',
        validators=[
            DataRequired(message='The field is required'),
            Length(
                min=min_string_value,
                max=max_string_value,
                message=f'From {min_string_value} to {max_string_value} characters'
            ),
            Regexp(regex='^AS[0-9]*$', message='Wrong ASN format'),
        ],
        render_kw={'class': 'form-control', 'placeholder': 'AS999'},
    )
    asset = StringField(label='ASSET', render_kw={'class': 'form-control', 'placeholder': 'AS-NINE'})
    remark = StringField(label='Remark', render_kw={'class': 'form-control', 'placeholder': 'Nine Ltd'})
    client = SelectField(
        label='Choose client',
        coerce=int,
        validators=[DataRequired(message='The field is required')],
        render_kw={'class': 'form-control'},
    )
