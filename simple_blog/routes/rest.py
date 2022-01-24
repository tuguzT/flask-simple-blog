from flask import request, jsonify
from flask_login import login_required, current_user

from .errors import RestError
from .. import app
from ..repository import db
from ..repository.model import Post, DeletedPosts, User


@app.route('/api/post/soft_delete', methods=['POST'])
@login_required
def soft_delete_post():
    user: User = current_user
    post_id = request.json['id']
    post: Post = Post.query.filter_by(id=post_id).one_or_none()
    if post is None:
        raise RestError(404, 'No user exists by provided id')
    if post.author != user:
        raise RestError(403, 'Cannot soft-delete post of another user')
    deleted_post = DeletedPosts.query.filter_by(post=post).one_or_none()
    if deleted_post is not None:
        raise RestError(403, 'Post was already soft-deleted, cannot soft-delete again')
    deleted_post = DeletedPosts(post=post)
    db.session.add(deleted_post)
    db.session.commit()
    return jsonify({'message': 'Post was soft-deleted successfully'})


@app.route('/api/post/restore', methods=['POST'])
@login_required
def restore_post():
    user: User = current_user
    post_id = request.json['id']
    post: Post = Post.query.filter_by(id=post_id).one_or_none()
    if post is None:
        raise RestError(404, 'No user exists by provided id')
    if post.author != user:
        raise RestError(403, 'Cannot restore post of another user')
    count: int = DeletedPosts.query.filter_by(post=post).delete()
    if count == 0:
        raise RestError(403, 'Post was not soft-deleted, cannot restore')
    db.session.commit()
    return jsonify({'message': 'Post was restored successfully'})
