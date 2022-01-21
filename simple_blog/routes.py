from flask import render_template

from data.user import User
from simple_blog import app


@app.route('/')
def index():
    user = User(name="Timur")
    return render_template('index.html', user=user)
