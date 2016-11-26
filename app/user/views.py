from . import user
from flask import render_template
from flask_login import login_required
from ..models import User
# from . import EditorProfileForm

@user.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username = username).first()
  if user is None:
    abort(404)
  return render_template('user/user.html', user=user)
# @user.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def editProfile():
#   form = EditorProfileForm()
  