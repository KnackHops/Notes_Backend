from flask import (
    Blueprint, request, make_response, current_app
)
import click
import json
from flaskr.db import (
    get_db, get_data
)

bp = Blueprint('user', __name__, url_prefix='/user')


def local_data_get(which):
    db = get_db(which)
    resp = get_data(**db)

    return json.loads(resp)


def find_user(data):
    found = None
    for user in data['record']:
        if user['username'] == request.json['username']:
            found = user
    return found


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = local_data_get('login')
        error = None
        error_code = None
        user = None

        if data is not None:
            user = find_user(data)
        else:
            error = 'Error getting data!'
            error_code = 500

        if error is None:
            if user is None:
                return 'register commence'
            else:
                error = 'User exist!'
                error_code = 404

        resp = make_response(({'errorMessage': error}, error_code))

        return resp

    return 'success'


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = local_data_get('login')
        error = None
        error_code = None
        user = None

        if data is not None:
            user = find_user(data)
        else:
            error = 'Error getting data!'
            error_code = 500

        if error is None:
            if user is not None:
                if user['password'] == request.json['password']:
                    data = local_data_get('profile')
                    user = find_user(data)

                    resp = make_response((user, 200))
                    return resp
                else:
                    error = 'Wrong password!'
            else:
                error = 'User does not exist!'

        if error is not None and error_code is None:
            error_code = 404

        resp = make_response(({'errorMessage': error}, error_code))

        return resp

    return 'success'


@bp.after_request
def after_request_func(response):
    response.headers['Content-Type'] = 'application/json'
    click.echo("yep")
    return response
