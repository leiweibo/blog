from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User

class LoginForm(Form):
    email = StringField('Email', validators = [Required(), Length(1, 64), Email()])

    password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class RegisterForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Register');

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user.')

class ChangePasswordForm(Form):
    password = PasswordField('Original Password', validators=[Required()])
    newPassword = PasswordField('New Password', validators=[Required(), EqualTo('newPassword2', message='Passwords must match.')])
    newPassword2 = PasswordField('Confirm New Password', validators=[Required()])
    submit = SubmitField('Change Password')

class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Submit')

class PasswordResetForm(Form):
    newPassword = PasswordField('New Password', validators=[Required(), EqualTo('newPassword2', message='Passwords must match.')])
    newPassword2 = PasswordField('Confirm New Password', validators=[Required()])
    submit = SubmitField('Submit')

class ChangeEmailRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Submit')    