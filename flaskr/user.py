import click
from flask import (
    Blueprint, request
)

from flaskr.db import (
    get_db,
)

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register')
def register():
    db = None

    # if request.method == 'POST':
    #     db = get_db('login')

    db = get_db('login')

    return f'<p>yip<p>'
