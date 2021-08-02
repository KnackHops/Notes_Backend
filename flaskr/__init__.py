import os
import click
from flask import (
    Flask, url_for
)
from flaskr.user import update_db_password


def create_app():
    # will work on login first
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    from . import notes
    from . import user

    for parent in (notes, user):
        app.register_blueprint(parent.bp)

    with app.test_request_context():
        pass
        # c = app.test_client()
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
        #             'email': 'test@gmail.com',
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
        #
        # print(req.data)
        # print(req.status)

    @click.command('up-db-ps')
    def update_pass():
        update_db_password()

    @click.command('hello-world')
    def hello_world():

        click.echo('hi')

    app.cli.add_command(update_pass)
    app.cli.add_command(hello_world)

    return app
