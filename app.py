from flask import Flask, request, make_response, render_template, session, redirect, url_for
import os

from flask.ext.bootstrap import Bootstrap

from flask.ext.moment import Moment
from datetime import datetime

from forms.BasicForm import NameForm

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

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name) 

if __name__ == '__main__':
    app.run(debug=True)