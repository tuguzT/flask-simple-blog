from flask import render_template

from simple_blog import app
from simple_blog.repository.model.user import User


@app.route('/')
def index():
    user: User = User.query.filter_by(name='Timur').first()
    print(user)
    return render_template('index.html', user=user)
