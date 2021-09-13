import os


class Config(object):
    Testing = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')