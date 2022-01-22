from flask import render_template, abort

from simple_blog import app
from simple_blog.repository.model.user import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name: str):
    user: User = User.query.filter_by(name=name).one_or_none() or abort(404)
    print(user)
    return render_template('user.html', title=user.name, user=user)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html', title='404 Not Found'), 404
