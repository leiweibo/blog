from flask import Flask, request, make_response, render_template
import os
from flask.ext.bootstrap import Bootstrap

template_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_path)
bootstrap = Bootstrap(app)

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
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name) 

if __name__ == '__main__':
    app.run(debug=True)