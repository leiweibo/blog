from flask_wtf import Form 
from wtforms import StringField, SubmitField, validators, TextField, TextAreaField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class RegistrationForm(Form):
    
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    content = TextAreaField(u'Mailing Content', [validators.optional(), validators.length(max=200)])  
    submit = SubmitField('Send')
    