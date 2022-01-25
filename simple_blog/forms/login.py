from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms_html5 import AutoAttrMeta


class LoginForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=48)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
