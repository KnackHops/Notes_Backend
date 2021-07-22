from flask import (
    Blueprint, request
)
import json
from flaskr.db import (
    get_db, get_data
)

bp = Blueprint('user', __name__, url_prefix='/user')


def data_get(which):
    db = get_db(which)
    resp = get_data(*db)

    return json.loads(resp)


def find_user(data):
    found = False
    for user in data['record']:
        if user['username'] == request.json['username']:
            found = True
    return found


@bp.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        data = data_get('login')
        error = None

        if data is not None:
            if find_user(data):
                error = 'User exists!'
        else:
            error = 'Error getting data!'

        if error is None:
            pass

    return f'<p>trying to register!<p>'


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = data_get('login')
        error = None

        if data is not None:
            if find_user(data):
                pass
            else:
                error = 'User does not exist!'
        else:
            error = 'Error getting data!'

        if error is None:
            pass

    return f'logging in'
