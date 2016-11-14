from flask import Flask, request, make_response, render_template, session, redirect, url_for, flash
import os

from flask.ext.bootstrap import Bootstrap

from flask.ext.moment import Moment
from datetime import datetime

from forms.BasicForm import NameForm

from flask.ext.sqlalchemy import SQLAlchemy

from shared import db
from models.models import User, Role

template_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_path)
app.config['SECRET_KEY'] = 'hard to guess string' ###TODO
#####db configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLCHEMY_COMMIT_ON_TEARDOWN'] = True
db.init_app(app)
# refer here
# http://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
# with app.app_context():
#     db.create_all()

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
        uName = form.name.data
        print('the user name posted is:' + uName)
        user = User.query.filter_by(username=uName).first()
        if user is None:
            user = User(username = uName)
            db.session.add(user)
            db.session.commit()
            print('db saved.......')
            session['known'] = False
        else:
            print('user exists.......')
            session['known'] = True
        
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name) 

if __name__ == '__main__':
    app.run(debug=True)

