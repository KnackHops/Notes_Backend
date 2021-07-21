import os
from flask import Flask


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

    return app
