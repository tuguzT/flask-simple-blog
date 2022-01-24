from flask import render_template
from flask_login import current_user, login_required

from .utils import posts_not_deleted, posts_deleted
from .. import app
from ..forms import AddPostForm
from ..repository import db
from ..repository.model import User, Post


@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)


# noinspection PyShadowingNames
@app.route('/me')
@login_required
def me():
    user: User = current_user
    posts: list[Post] = posts_not_deleted().filter(Post.author == user).all()
    return render_template('user.html', title=user.name, user=user, posts=posts)


# noinspection PyShadowingNames
@app.route('/me/deleted_posts')
def deleted_posts():
    user: User = current_user
    deleted_posts: list[Post] = posts_deleted().filter(Post.author == user).all()
    return render_template('deleted_posts.html', title='Deleted posts', current_user=user, deleted_posts=deleted_posts)


# noinspection PyShadowingNames
@app.route('/user/<name>')
def user(name: str):
    user: User = User.query.filter_by(name=name).first_or_404(description=f'No user with username {name}')
    posts: list[Post] = posts_not_deleted().filter(Post.author == user).all()
    return render_template('user.html', title=user.name, user=user, current_user=current_user, posts=posts)


# noinspection PyShadowingNames
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    user: User = current_user

    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text_content=form.text_content.data, author=user)
        db.session.add(post)
        db.session.commit()

    posts: list[Post] = posts_not_deleted().order_by(Post.created_at).all()
    return render_template('posts.html', title='All posts', current_user=user, posts=posts, form=form)
