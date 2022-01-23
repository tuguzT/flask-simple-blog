from urllib.parse import urljoin, urlparse

from flask import render_template, abort, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from . import app
from .forms import LoginForm
from .repository import db
from .repository.model import Session, User


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(name=form.username.data).one_or_none()
        if user is None:
            flash('User with provided username does not exist!')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid password for the user with provided username!')
            return redirect(url_for('login'))

        session: Session = Session.query.with_parent(user).one_or_none()
        if session is None:
            session = Session(user=user)
            db.session.add(session)
            db.session.commit()
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or not is_safe_url(next_page):
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/me')
@login_required
def me():
    user: User = current_user
    return render_template('user.html', title=user.name, user=user)


@app.route('/user/<name>')
def user(name: str):
    user: User = User.query.filter_by(name=name).one_or_none() or abort(404)
    return render_template('user.html', title=user.name, user=user)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html', title='404 Not Found'), 404
