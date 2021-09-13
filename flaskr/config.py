import os


class Config(object):
    Testing = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.environ.get('DATABASE_URL')}?ssl=true"