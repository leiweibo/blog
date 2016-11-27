from flask import render_template, session, redirect, url_for, current_app
from flask_login import current_user
from .. import db
from ..models import Post, Permission
from ..email import send_email
from . import main
from .forms import PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body = form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts = posts)
