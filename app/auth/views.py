from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailRequestForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..models import User, Permission
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..email import send_email
from flask import current_app

@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)

    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirmed Your Acct', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))
# @auth.route('/secret')
# @login_required
# def secret():
#     return 'Only authenticated users are allowed!

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
            current_user.ping()
            if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.'\
                and request.endpoint != 'static':
                return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed: 
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm') 
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.') 
    return redirect(url_for('main.index'))

@auth.route('/change_passowrd', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if not user.verify_password(form.password.data):
            flash('The origin password incorrect!')
            return redirect(url_for('auth.change_password'))
        user.password = form.newPassword.data
        db.session.add(user)
        db.session.commit()
        logout_user()
        return render_template('auth/change_password_suc.html')
    return render_template('auth/change_password.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect('main.index')

    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('The email address is incorrect!')
        else:
            token = user.generate_reset_token()
            send_email(form.email.data, 
                'Reset Your Password', 'auth/email/reset_password', 
                user = user, token=token,
                next=request.args.get('next'))
            flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY']) 
        try:
            data = s.loads(token)
        except:
            return redirect(url_for('main.index'))
        user = User.query.filter_by(email=data.get('email')).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.newPassword.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            flash('Your password update failed.')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailRequestForm()
    if form.validate_on_submit():
        newEmail = form.email.data
        user = User.query.filter_by(email=newEmail).first()
        if not user is None:
            flash('The email has been used by other users.')
            return redirect(url_for('auth.change_email_request'))
        token = current_user.generate_change_email_token(new_email = newEmail)
        send_email(newEmail,'Change Your Email', 'auth/email/change_email', user=current_user, token=token)
        flash('An email with instructions to change your email has been sent to you.') 
        return redirect(url_for('main.index'))
    return render_template('auth/change_email.html', form =form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    user = current_user
    if user.change_email(token):
        flash('You email have been changed.')
    else:
        flash('email change failed.')
    return redirect(url_for('main.index'))

