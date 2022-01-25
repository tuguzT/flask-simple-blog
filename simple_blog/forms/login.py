from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms_html5 import AutoAttrMeta

from ..repository.model import User


class LoginForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=48)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user: User | None = None

    def validate_username(self, username: StringField):
        self.user = User.query.filter_by(name=username.data).one_or_none()
        if self.user is None:
            raise ValidationError('User with provided username does not exist')

    def validate_password(self, password: PasswordField):
        if self.user is not None and not self.user.check_password(password.data):
            raise ValidationError('Invalid password for the user with provided username')
