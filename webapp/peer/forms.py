from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class PeerForm(FlaskForm):
    render_kw = {"class": "form-control"}

    asn = StringField(
        label='Номер AS',
        validators=[
            DataRequired(message="Поле обязательно для заполнения"),
            Length(min=5, max=13, message=f"Количество симовлов должно быть от 5 до 13"),
            Regexp(regex='^AS[0-9]*$', message="Неверный формат AS-NUM"),
        ],
        render_kw={"class": "form-control"}
    )
    asset = StringField(label='AS-SET', render_kw=render_kw)
    remark = StringField(label='Описание', render_kw=render_kw)
    current_prefixes = StringField(label='Актуальные префиксы', render_kw=render_kw)
    new_prefixes = StringField(label='Новые префиксы', render_kw=render_kw)
    todelete_prefixes = StringField(label='Префиксы для удаления', render_kw=render_kw)
    submit = SubmitField(label='Save', render_kw={"class": "btn btn-primary"})
