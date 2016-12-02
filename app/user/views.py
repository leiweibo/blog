from . import user
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from ..models import User, Post, Permission
from ..decorators import permission_required
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

#todo
@user.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    u = User.query.filter_by(username=username).first();
    if u is None:
        flash('Invalid User')
        return redirect(url_for('main.index'))
    if current_user.is_following(u):
        flash('You are already following this user.')
        return redirect('.user', username=username)
    current_user.follow(u)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@user.route('/unfollow/<username>')
def unfollow(username):
    u = User.query.filter_by(username=username).first();
    if u is None:
        flash('Invalid User')
        return redirect(url_for('main.index'))
    current_user.unfollow(u) 
    flash('You are now not following %s.' % username)
    return redirect(url_for('.user', username=username))

@user.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
        for item in pagination.items]

    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)

#todo
@user.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWINGS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
        for item in pagination.items]

    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@user.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user/user.html', user=user, posts = posts)

