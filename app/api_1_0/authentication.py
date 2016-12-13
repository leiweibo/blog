from flask import g, jsonify, session, request
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from ..models import User, AnonymousUser
from . import api
from .errors import forbidden, unauthorized

tokenAuth = HTTPTokenAuth(scheme='Bearer')
basicAuth = HTTPBasicAuth()

@basicAuth.verify_password
def verify_password(email_or_token, password):
  if email_or_token == '':
    g.current_user = AnonymousUser()
    return True
  if password == '':
    g.current_user = User.verify_auth_token(email_or_token)
    g.token_used = True
    return g.current_user is not None
  user = User.query.filter_by(email = email_or_token).first()
  if not user:
    return False
  g.current_user = user
  g.token_used = False
  return user.verify_password(password)

@tokenAuth.error_handler
@basicAuth.error_handler
def auth_error():
  return unauthorized('Invalid credentials')

@tokenAuth.verify_token
def verify_token(token):
  g.current_user = None
  g.current_user = User.verify_auth_token(token)
  return True

@api.before_request
@tokenAuth.login_required
def before_request():
  print("the endpoint is:" + request.endpoint)
  if 'logged_in' not in session and request.endpoint != 'api.get_token':
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
      return forbidden('Uncofirmed account')

#encoded = base64.b64encode(b'leiweibo@gmail.com:xxxx')
@api.route('/token')
@basicAuth.login_required
def get_token():
    if g.current_user.is_anonymous or g.token_used: 
      return unauthorized('Invalid credentials')
    #there is no decode in the sample code.  
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600).decode('ascii'), \
      'expiration': 3600})

