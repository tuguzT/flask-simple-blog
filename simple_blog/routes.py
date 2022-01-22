from flask import render_template

from simple_blog import app
from simple_blog.repository.model.user import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name: str):
    user: User = User.query.filter_by(name=name).one()
    print(user)
    return render_template('user.html', title=user.name, user=user)
