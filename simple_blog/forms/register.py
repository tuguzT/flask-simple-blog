from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from wtforms_html5 import AutoAttrMeta

from ..repository.model import User


class RegisterForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=48)])
    repeat_password = PasswordField('Repeat password',
                                    validators=[DataRequired(), Length(min=4, max=48), EqualTo('password')])
    submit = SubmitField('Register')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username: StringField):
        user: User | None = User.query.filter_by(name=username.data).one_or_none()
        if user is not None:
            raise ValidationError(f'User with provided username already exists')
