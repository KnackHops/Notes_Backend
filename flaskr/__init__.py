import os
# import click
from flask import (
    Flask, url_for
)


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
        c = app.test_client()
        req = c.post(
            url_for('user.login'),
            content_type='application/json',
            json={
                'username': 'affafu',
                'password': 'affafuPass'
            }
        )

        print(req.data)
        print(req.status)

    return app
