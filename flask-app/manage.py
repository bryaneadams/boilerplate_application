from flask import Flask, url_for, render_template, redirect, session, request, flash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from flask_migrate import Migrate
import os
import requests
from urllib3.exceptions import InsecureRequestWarning

from flask_oidc import OpenIDConnect

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from boilerplate import *
from boilerplate.utils import UserCredentials

app = create_app()

app.app_context().push()

from boilerplate.boilerform.boilerform import boilerform_blueprint

from boilerplate.model import *

app.register_blueprint(boilerform_blueprint)

'''
Login manger keeps track of who is logged into the application
I also use this in the templates to see if they have the correct
Access to each resources
'''
login_manager = LoginManager()
login_manager.init_app(app)

oidc = OpenIDConnect(app)

@app.route('/splash')
def splash():
    '''
    Until I figure out another way to grab the token each time
    You need to log the user out to clear all the cookies.

    This removes the session cookie, which you need to do
    when you update the deployment. Updating the deployment
    will remove the user from the Login Manager. This prevents them
    from being able to visit other pages.
    '''
    oidc.logout()
    return render_template('splash.html')

@app.route('/login')
@oidc.require_login
def login():
    '''
    Example for protected endpoint that extracts private information from the OpenID Connect id_token.
    Uses the accompanied access_token to access a backend service.
    '''

    '''
    jwt encrypted token
    contains the information for the roles they have
    to each applications
    '''

    access_token = oidc.get_access_token()

    print(f"#### access_token {access_token}", flush=True)

    '''
    get the user information
    '''

    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    print(f"### INFO {info}", flush = True)
    current_user={
        'username': info.get('preferred_username'),
        'email': info.get('email')
    }

    '''
    This is in `/boilerplate/utils.py` and checks what roles the user
    has access to. If you update a user's roles, they will need to 
    logout and log back in.
    '''
    user_details=UserCredentials(current_user, access_token, os.getenv('OIDC_CLIENT_ID'))

    '''
    Check to see if they have rights to use this application
    '''
    if not user_details.is_app_user():
        return redirect(url_for('not_app_user'))
    
    '''
    Update user information with roles
    '''

    current_user['admin']=user_details.is_app_admin()
    
    check_user = User.query.filter_by(email=user_details.user_email).first()
    if not check_user:
        create_user = User(**current_user)
        db.session.add(User(**current_user))
        db.session.commit()
        check_user = User.query.filter_by(email=user_details.user_email).first()
        login_user(check_user)
    else:
        login_user(check_user)
    
    return redirect('/')

@app.route('/')
#@login_required
def home():
    title = 'Main Page'
    return render_template('landing.html', title=title)  

@app.route('/api', methods=['POST'])
@oidc.accept_token(require_token=True, scopes_required=['openid'])
def hello_api():
    """OAuth 2.0 protected API endpoint accessible via AccessToken"""

    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout')
def logout():
    """Performs local logout by removing the session cookie."""

    oidc.logout()
    logout_user()
    return redirect(url_for('splash'))

'''
These two functions are required for the Login Manager
https://flask-login.readthedocs.io/en/latest/
'''

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must login to access this page', category='error')
    return redirect(url_for('splash'))

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        user = User.query.get(int(user_id))
        return user


migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')