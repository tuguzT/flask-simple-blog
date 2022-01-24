from flask import request, jsonify
from flask_login import login_required

from .. import app
from ..repository import db
from ..repository.model import Post, DeletedPosts


@app.route('/api/post/soft_delete', methods=['POST'])
@login_required
def soft_delete_post():
    post_id = request.json['id']
    post: Post = Post.query.filter_by(id=post_id).first_or_404()
    deleted_post = DeletedPosts(post=post)
    db.session.add(deleted_post)
    db.session.commit()
    return jsonify({'message': 'Post was soft-deleted'})
