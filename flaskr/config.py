import os


class Config(object):
    Testing = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://postgres:" \
                              f"{os.environ.password_key}@" \
                              f"{os.environ.get('DATABASE_URL')}"