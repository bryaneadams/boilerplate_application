import os
import secrets

class Config:
    DEBUG=False
    POSTGRES_USER=os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB=os.getenv('POSTGRES_DB')
    POSTGRES_HOST=os.getenv('POSTGRES_HOST')
    DB_PORT=os.getenv('DB_PORT')
    SECRET_KEY=secrets.token_urlsafe(64)

class DevelopmentConfig(Config):
    DEBUG=True
    POSTGRES_USER=os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB=os.getenv('POSTGRES_DB')
    POSTGRES_HOST=os.getenv('POSTGRES_HOST')
    DB_PORT=os.getenv('DB_PORT')
    SECRET_KEY="shhh"
    SQLALCHEMY_TRACK_MODIFICATIONS = False