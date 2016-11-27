from . import user
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Post
from .. import db
from .forms import EditorProfileForm

@user.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditorProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('You profile has been changed')
        return redirect(url_for('.user', username = current_user.username))

    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me ##temp typo abount_me
    return render_template('user/edit_profile.html', form = form)


@user.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user/user.html', user=user, posts = posts)

