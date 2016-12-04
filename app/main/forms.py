from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(Form):
  body = PageDownField("What's on your mind?", validators=[Required()])
  submit = SubmitField('Submit');

class CommentForm(Form):
  body = StringField('', validators=[Required()])
  submit = SubmitField('Submit')