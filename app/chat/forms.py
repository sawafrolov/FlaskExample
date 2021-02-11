from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Your message'), validators=[DataRequired(), Length(min=1, max=240)])
    submit = SubmitField(_l('Submit'))
