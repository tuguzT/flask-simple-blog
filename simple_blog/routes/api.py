from flask import request, jsonify
from flask_login import current_user

from .errors import ApiError, FormValidationError
from .. import app
from ..forms import AddPostForm
from ..repository import db
from ..repository.model import Post, DeletedPosts, User


def validate_current_user() -> User:
    user: User = current_user
    if not user.is_authenticated:
        raise ApiError(401, 'User was not authenticated')
    return user


def validate_post(post_id: str) -> Post:
    validate_current_user()
    post: Post = Post.query.filter_by(id=post_id).one_or_none()
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
    return jsonify(post)


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
