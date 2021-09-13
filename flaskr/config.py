import os


class Config(object):
    Testing = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://" \
                              f"{os.environ.get('User')}:" \
                              f"{os.environ.get('Password')}@{os.environ.get('DATABASE_URL')}"