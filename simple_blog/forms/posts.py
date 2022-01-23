from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text_content = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Add post')
