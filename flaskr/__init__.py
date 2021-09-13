import os
import click
from flask import Flask
from flaskr.db import init_db
# from flaskr.db import (
#     add_test, query_test, update_test
# )
from flask_cors import (
    CORS,
)
from flask_sqlalchemy import SQLAlchemy
from instance.config import DevelopmentConfig
from instance.config import ProductionConfig

_sq = None
_User = None
_Login = None
_ProfileUpdate = None
_Note = None


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={
        r'/user/*': {
            'origins': '*'
        }
    })

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    try:
        os.mkdir('flaskr/temp')
    except OSError:
        pass

    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object(DevelopmentConfig())
    elif os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig())

    global _sq
    global _User
    global _Login
    global _ProfileUpdate
    global _Note

    _sq = SQLAlchemy(app)
    _User, _Login, _ProfileUpdate, _Note = init_db(_sq)

    # test local
    if os.path.isfile('temp/temp.db') and os.environ.get('FLASK_ENV') == 'development':
        _sq.create_all()
    # _sq.create_all()

    from . import notes
    from . import user

    for parent in (notes, user):
        app.register_blueprint(parent.bp)

    app.add_url_rule('/', endpoint='index')

    with app.test_request_context():
        pass
        c = app.test_client()

        # req = c.post(
        #     url_for('user.profile_get'),
        #     content_type='application/json',
        #     json={
        #         'username': 'affafu',
        #     }
        # )

        # req_2 = c.post(
        #     url_for('user.profile_save'),
        #     content_type='application/json',
        #     json={
        #         'username': 'affafu',
        #         'pfp': "newPFP",
        #         'pfpLast': "yip"
        #     }
        # )

        # req = c.post(
        #     url_for('notes.fetch_all'),
        #     content_type='application/json',
        #     json={
        #         'user': 'asdads'
        #     }
        # )

        # req = c.post(
        #     url_for('notes.edit_note'),
        #     content_type='application/json',
        #     json={
        #         'note': {
        #             'title': 'test from backend',
        #             'body': 'test from backend nga',
        #             'user': 'affafu',
        #             'id': 0
        #         }
        #     }
        # )

        # req = c.post(
        #     url_for('user.register'),
        #     content_type='application/json',
        #     json={
        #         'login_data': {
        #             'username': 'test',
        #             'password': 'testPass'
        #         },
        #         'user_data': {
        #             'username': 'test',
        #             'email': 'testin@gmail.com',
        #             'mobile': None,
        #             'pfp': 'default',
        #             'nickname': 'test me'
        #         },
        #         'profile_data': {
        #             'username': 'test',
        #             'pfpLast': {
        #                 'month': 12,
        #                 'day': 5,
        #                 'year': 2020
        #             },
        #             'nickLast': {
        #                 'month': 12,
        #                 'day': 5,
        #                 'year': 2020
        #             }
        #         }
        #     }
        # )
        # #
        # print(req.data)
        # print(req.status)
        # print(req_2.data)
        # print(req_2.status)

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