import os
import click
from flask import Flask
from . import notes
from . import user
from flaskr.db import init_db
# from flaskr.db import (
#     add_test, query_test, update_test
# )
from flaskr.config import Config
from flask_cors import (
    CORS,
)
from flask_sqlalchemy import SQLAlchemy

# if os.environ.get('FLASK_ENV') == 'development':
#     app = Flask(__name__, instance_relative_config=True)
#     if os.environ.get('WHICH_DB') == 'localhost':
#         from instance.config import DevelopmentConfigLocalhost
#
#         app.config.from_object(DevelopmentConfigLocalhost())
#     else:
#         from instance.config import DevelopmentConfigSQLite
#
#         app.config.from_object(DevelopmentConfigSQLite())
#
#         try:
#             os.mkdir('flaskr/temp')
#         except OSError:
#             pass
#
#     try:
#         os.mkdir(app.instance_path)
#     except OSError:
#         pass
# else:
#     app = Flask(__name__, instance_relative_config=False)
#     app.config.from_object(Config())

app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config())
CORS(app, resources={
        r'/user/*': {
            'origins': '*'
        }
})

_sq = SQLAlchemy(app)
_User, _Login, _ProfileUpdate, _Note = init_db(_sq)

for parent in (notes, user):
    app.register_blueprint(parent.bp)

app.add_url_rule('/', endpoint='index')

# _sq = None
# _User = None
# _Login = None
# _ProfileUpdate = None
# _Note = None


def create_app():
    # app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object(Config())

    # if os.path.isfile('temp/temp.db') and os.environ.get('FLASK_ENV') == 'development':
    #     _sq.create_all()
    # @click.command('up-db-user')
    # def update_pass():
    #     update_db_users()
    #
    # @click.command('hello-world')
    # def hello_world():
    #     click.echo('hi')
    #
    # @click.command('up-no-cmd')
    # def up_no_note():
    #     update_note_cmd()

    @click.command('dbase-check')
    def dbase_check():
        pass
        # add_test()
        # query_test()
        # update_test()

    # app.cli.add_command(update_pass)
    # app.cli.add_command(hello_world)
    # app.cli.add_command(up_no_note)
    # app.cli.add_command(dbase_check)
    click.echo(app)
    return app
