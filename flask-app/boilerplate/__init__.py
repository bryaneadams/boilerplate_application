from flask import Flask
from .config import *
from .model import *
from .utils import *
from time import sleep
import json

import os

def create_app():
    app = Flask(__name__)

    config = DevelopmentConfig
    app.config.from_object(config)

    '''
    flask_oidc requires a json for your secrets.
    I use python for simplicty to create the secrets and then
    write them to the proper location
    This is so people only have to change their .env file
    '''

    client_secrets = {
    "web": {
        "issuer": f"{os.getenv('KEYCLOAK_URL')}/auth/realms/{os.getenv('KEYCLOAK_REALM')}",
        "auth_uri": f"{os.getenv('KEYCLOAK_URL')}/auth/realms/{os.getenv('KEYCLOAK_REALM')}/protocol/openid-connect/auth",
        "client_id": f"{os.getenv('KEYCLOAK_CLIENT_ID')}",
        "client_secret": f"{os.getenv('KEYCLOAK_SECRET')}",
        "redirect_uris": [
            "*"
        ],
        "userinfo_uri": f"{os.getenv('KEYCLOAK_URL')}/auth/realms/{os.getenv('KEYCLOAK_REALM')}/protocol/openid-connect/userinfo", 
        "token_uri": f"{os.getenv('KEYCLOAK_URL')}/auth/realms/{os.getenv('KEYCLOAK_REALM')}/protocol/openid-connect/token",
        "token_introspection_uri": f"{os.getenv('KEYCLOAK_URL')}/auth/realms/{os.getenv('KEYCLOAK_REALM')}/protocol/openid-connect/token/introspect"
        }
    }

    with open("client_secrets.json", "w") as outfile: 
        json.dump(client_secrets, outfile)

    app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': './client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': True,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'flask-demo',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
    })

    URI=f"postgresql://{app.config['POSTGRES_USER']}:{app.config['POSTGRES_PASSWORD']}@{app.config['POSTGRES_HOST']}:{app.config['DB_PORT']}/{app.config['POSTGRES_DB']}"

    app.config['SQLALCHEMY_DATABASE_URI'] = URI

    db.init_app(app)

    with app.app_context():
        '''
        This wait statement is here so when using docker-compose
        You will keep waiting for the database to start

        If you do not include this it will fail to connect to the db
        and stop

        This does not really matter to much in k8s
        '''
        num_retries = 10
        sleep_time = 3
        for _ in range(0, num_retries):
            try:
                db.create_all()
            except:
                print(f"failed {_+1} attempt(s) to connect to database.", flush=True)
                sleep(sleep_time)

    return app