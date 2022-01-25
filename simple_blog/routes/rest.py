from flask import request, jsonify
from flask_login import current_user

from .errors import RestError
from .. import app
from ..repository import db
from ..repository.model import Post, DeletedPosts, User


def validate_current_user() -> User:
    user: User = current_user
    if not user.is_authenticated:
        raise RestError(401, 'User was not authenticated')
    return user


def validate_post(post_id: str) -> Post:
    validate_current_user()
    post: Post = Post.query.filter_by(id=post_id).one_or_none()
    if post is None:
        raise RestError(404, 'No post exists by provided ID')
    return post


@app.route('/api/post/soft_delete', methods=['POST'])
def soft_delete_post():
    post_id = request.json['id']
    post = validate_post(post_id)
    if post.author != current_user:
        raise RestError(403, 'Cannot soft-delete post of another user')
    deleted_post = DeletedPosts.query.filter_by(post=post).one_or_none()
    if deleted_post is not None:
        raise RestError(403, 'Post was already soft-deleted, cannot soft-delete again')
    deleted_post = DeletedPosts(post=post)
    db.session.add(deleted_post)
    db.session.commit()
    return jsonify({'message': 'Post was soft-deleted successfully'})


@app.route('/api/post/delete', methods=['POST'])
def delete_post():
    post_id = request.json['id']
    post = validate_post(post_id)
    if post.author != current_user:
        raise RestError(403, 'Cannot delete post of another user')
    deleted_post = DeletedPosts.query.filter_by(post=post).one_or_none()
    if deleted_post is None:
        raise RestError(403, 'Post was never soft-deleted, cannot delete')
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post was deleted successfully'})


@app.route('/api/post/restore', methods=['POST'])
def restore_post():
    post_id = request.json['id']
    post = validate_post(post_id)
    if post.author != current_user:
        raise RestError(403, 'Cannot restore post of another user')
    count: int = DeletedPosts.query.filter_by(post=post).delete()
    if count == 0:
        db.session.rollback()
        raise RestError(403, 'Post was not soft-deleted, cannot restore')
    db.session.commit()
    return jsonify({'message': 'Post was restored successfully'})
