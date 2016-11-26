from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo

class EditorProfileForm(Form):
  name = StringField('Real Name', validators = [Length(0, 64)])
  location = StringField('Location', validators = [Length(0, 64)])
  about_me = TextAreaField('About me')
  submit = SubmitField('Submit')