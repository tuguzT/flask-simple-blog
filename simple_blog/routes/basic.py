from flask import render_template
from flask_login import current_user, login_required

from .utils import posts_not_deleted
from .. import app
from ..forms import AddPostForm
from ..repository import db
from ..repository.model import User, Post


# noinspection PyShadowingNames
@app.route('/')
def index():
    user: User = current_user
    return render_template('index.html', user=user)


# noinspection PyShadowingNames
@app.route('/me')
@login_required
def me():
    user: User = current_user
    posts: list[Post] = posts_not_deleted().filter(Post.author == user).all()
    return render_template('user.html', title=user.name, user=user, posts=posts)


# noinspection PyShadowingNames
@app.route('/user/<name>')
def user(name: str):
    user: User = User.query.filter_by(name=name).first_or_404(description=f'No user with username {name}')
    posts: list[Post] = posts_not_deleted().filter(Post.author == user).all()
    return render_template('user.html', title=user.name, user=user, posts=posts)


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
    return render_template('posts.html', title='All posts', posts=posts, user=user, form=form)
