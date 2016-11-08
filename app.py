from flask import Flask, request, make_response, render_template
import os

from flask.ext.bootstrap import Bootstrap

from flask.ext.moment import Moment
from datetime import datetime

from flask.ext.wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required])
    submit = SubmitField('Submit')

template_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_path)
app.config['SECRET_KEY'] = 'hard to guess string' ###TODO
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500    

@app.route('/')
def index():
    # response = make_response('<h1> This document carries a cookie!</h1>')
    # response.set_cookie('answer', '42')
    # return response
    return render_template('index.html', form=NameForm())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name) 

if __name__ == '__main__':
    app.run(debug=True)