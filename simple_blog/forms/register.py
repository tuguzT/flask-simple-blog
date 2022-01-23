from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from ..repository.model import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username: StringField):
        username = username.data
        user: User = User.query.filter_by(name=username).one_or_none()
        if user is not None:
            raise ValidationError(f'User with provided username {username} already exists')
