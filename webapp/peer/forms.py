from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class PeerForm(FlaskForm):
    asn = StringField(
        label='Номер AS',
        validators=[
            DataRequired(message="Поле обязательно для заполнения"),
            Length(min=5, max=13, message=f"Количество симовлов должно быть от 5 до 13"),
            Regexp(regex='^AS[0-9]*$', message="Неверный формат AS-NUM"),
        ],
        render_kw={"class": "form-control"}
    )
    asset = StringField(label='AS-SET', render_kw={"class": "form-control"})
    client = StringField(label='Название клиента', render_kw={"class": "form-control"})
    remark = StringField(label='Описание', render_kw={"class": "form-control"})
    current_prefixes = StringField(label='Актуальные префиксы', render_kw={"class": "form-control"})
    new_prefixes = StringField(label='Новые префиксы', render_kw={"class": "form-control"})
    todelete_prefixes = StringField(label='Префиксы для удаления', render_kw={"class": "form-control"})
    submit = SubmitField(label='Save', render_kw={"class": "btn btn-primary"})
