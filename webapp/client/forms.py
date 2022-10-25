from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp


class ClientForm(FlaskForm):
    render_kw = {"class": "form-control"}

    name = StringField('Название клиента', validators=[DataRequired()], render_kw=render_kw)


class ClentPeerForm(FlaskForm):
    render_kw = {"class": "form-control"}
    min_string_value = 5
    max_string_value = 13
    asn = StringField(
        label='Номер AS',
        validators=[
            DataRequired(message='Поле обязательно для заполнения'),
            Length(
                min=min_string_value,
                max=max_string_value,
                message=f'Количество симовлов должно быть от {min_string_value} до {max_string_value}'
            ),
            Regexp(regex='^AS[0-9]*$', message='Неверный формат AS-NUM'),
        ],
        render_kw=render_kw
    )
    asset = StringField(label='AS-SET', render_kw=render_kw)
    remark = StringField(label='Описание', render_kw=render_kw)
