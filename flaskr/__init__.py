import os
import click
from flask import Flask
from flaskr.db import init_db
# from flaskr.db import (
#     add_test, query_test, update_test
# )
from flaskr.config import Config
from flask_cors import (
    CORS,
)
from flask_sqlalchemy import SQLAlchemy

_sq = None
_User = None
_Login = None
_ProfileUpdate = None
_Note = None


def create_app():
    # if os.environ.get('FLASK_ENV') == 'development':
    #     app = Flask(__name__, instance_relative_config=True)
    #     if os.environ.get('WHICH_DB') == 'localhost':
    #         from instance.config import DevelopmentConfigLocalhost
    #         app.config.from_object(DevelopmentConfigLocalhost())
    #     else:
    #         from instance.config import DevelopmentConfigSQLite
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

    global _sq
    global _User
    global _Login
    global _ProfileUpdate
    global _Note

    _sq = SQLAlchemy(app)
    _User, _Login, _ProfileUpdate, _Note = init_db(_sq)

    # if os.path.isfile('temp/temp.db') and os.environ.get('FLASK_ENV') == 'development':
    #     _sq.create_all()

    from . import notes
    from . import user

    for parent in (notes, user):
        app.register_blueprint(parent.bp)

    app.add_url_rule('/', endpoint='index')

    @app.route('/')
    def index():
        return '<h1> Hello! <h1>'

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

    return app

if __name__ == '__main__':
    from flaskr import app

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)