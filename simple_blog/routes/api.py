from flask import request, jsonify, url_for
from flask_login import current_user, login_user

from .errors import ApiError, FormValidationError
from .utils import is_safe_url
from .. import app
from ..forms import AddPostForm, LoginForm, RegisterForm
from ..repository import db
from ..repository.model import Post, DeletedPosts, User, Session


def validate_current_user() -> User:
    user: User = current_user
    if not user.is_authenticated:
        raise ApiError(401, 'User was not authenticated')
    return user


def validate_user(user_id: str) -> User:
    validate_current_user()
    user: User | None = User.query.get(user_id)
    if user is None:
        raise ApiError(404, 'No user exists by provided ID')
    return user


def validate_post(post_id: str) -> Post:
    validate_current_user()
    post: Post | None = Post.query.filter_by(id=post_id).one_or_none()
    if post is None:
        raise ApiError(404, 'No post exists by provided ID')
    return post


@app.route('/api/post/soft_delete', methods=['POST'])
def soft_delete_post():
    post_id = request.json['id']
    post = validate_post(post_id)
    if post.author != current_user:
        raise ApiError(403, 'Cannot soft-delete post of another user')
    deleted_post = DeletedPosts.query.filter_by(post=post).one_or_none()
    if deleted_post is not None:
        raise ApiError(403, 'Post was already soft-deleted, cannot soft-delete again')
    deleted_post = DeletedPosts(post=post)
    db.session.add(deleted_post)
    db.session.commit()
    return jsonify({'message': 'Post was soft-deleted successfully'})


@app.route('/api/post/delete', methods=['POST'])
def delete_post():
    post_id = request.json['id']
    post = validate_post(post_id)
    if post.author != current_user:
        raise ApiError(403, 'Cannot delete post of another user')
    deleted_post = DeletedPosts.query.filter_by(post=post).one_or_none()
    if deleted_post is None:
        raise ApiError(403, 'Post was never soft-deleted, cannot delete')
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post was deleted successfully'})


@app.route('/api/post/restore', methods=['POST'])
def restore_post():
    post_id = request.json['id']
    post = validate_post(post_id)
    if post.author != current_user:
        raise ApiError(403, 'Cannot restore post of another user')
    count: int = DeletedPosts.query.filter_by(post=post).delete()
    if count == 0:
        db.session.rollback()
        raise ApiError(403, 'Post was not soft-deleted, cannot restore')
    db.session.commit()
    return jsonify({'message': 'Post was restored successfully'})


@app.route('/api/post/<post_id>')
def get_post(post_id: str):
    post = validate_post(post_id)
    data = {
        'id': post.id,
        'created_at': post.created_at,
        'title': post.title,
        'text_content': post.text_content,
        'author_id': post.author_id,
    }
    return jsonify(data)


@app.route('/api/user/<user_id>')
def get_user(user_id: str):
    user = validate_user(user_id)
    data = {
        'id': user.id,
        'name': user.name,
    }
    return jsonify(data)


@app.route('/api/post/form/add', methods=['POST'])
def add_post_form():
    user = validate_current_user()
    form = AddPostForm()
    if not form.is_submitted():
        raise ApiError(403, 'Post creation form was not submitted')
    if not form.validate():
        raise FormValidationError(form, 403, 'Post creation form contains errors after validation')
    post = Post(title=form.title.data, text_content=form.text_content.data, author=user)
    db.session.add(post)
    db.session.commit()
    return jsonify({
        'message': 'Post was created successfully',
        'id': post.id,
    })


@app.route('/api/login/form', methods=['POST'])
def login_form():
    form = LoginForm()
    if not form.is_submitted():
        raise ApiError(403, 'Login form was not submitted')
    if not form.validate():
        raise FormValidationError(form, 403, 'Login form contains errors after validation')
    user: User = User.query.filter_by(name=form.username.data).one()

    session: Session = Session.query.with_parent(user).one_or_none()
    if session is None:
        session = Session(user=user)
        db.session.add(session)
        db.session.commit()
    login_user(user, remember=form.remember_me.data)

    next_page = request.args.get('next')
    if not next_page or not is_safe_url(next_page):
        next_page = url_for('index')
    data = {
        'url': next_page,
        'message': 'User logged in successfully',
    }
    return jsonify(data)


@app.route('/api/register/form', methods=['POST'])
def register_form():
    form = RegisterForm()
    if not form.is_submitted():
        raise ApiError(403, 'Register form was not submitted')
    if not form.validate():
        raise FormValidationError(form, 403, 'Register form contains errors after validation')

    # noinspection PyArgumentList
    user = User(name=form.username.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    data = {
        'url': url_for('login'),
        'message': 'User registered successfully',
    }
    return jsonify(data)
