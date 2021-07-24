from flask import (
    Blueprint, request, make_response
)
import click
import json
from flaskr.db import (
    get_db, get_data, update_data
)

bp = Blueprint('user', __name__, url_prefix='/user')


def local_data_get(which):
    db = get_db(which)
    resp = get_data(**db)

    return_var = {
        'url_meta': db,
        'data': json.loads(resp)
    }

    return return_var


def find_user(data, username):
    found = None
    for user in data['record']:
        if user['username'] == username:
            found = user
    return found


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login_data = local_data_get('login')
        error = None
        error_code = None
        user = None

        if login_data is not None:
            user = find_user(login_data['data'], request.json['login_data']['username'])
        else:
            error = 'Error getting data!'
            error_code = 500

        if error is None:
            if user is None:
                user_data = local_data_get('user')
                profile_data = local_data_get('profile')
                list_db_metadata = [
                    login_data['url_meta'],
                    user_data['url_meta'],
                    profile_data['url_meta']
                ]
                list_db = [
                    login_data['data'],
                    user_data['data'],
                    profile_data['data']
                ]
                list_request_var = [
                    'login_data',
                    'user_data',
                    'profile_data'
                ]
                x = 0
                response_update = []
                for each_url in list_db_metadata:
                    each_url['headers']['Content-Type'] = 'application/json'
                    response_update.append(
                        update_data(**each_url, data=list_db[x], new_data=request.json[list_request_var[x]])
                    )
                    x = x + 1

                print(list_db_metadata[0]['headers'])
                return 'register commence'
            else:
                error = 'User exist!'
                error_code = 302

        resp = make_response(({'errorMessage': error}, error_code))

        return resp

    return 'success'


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login_data = local_data_get('login')
        error = None
        error_code = None
        user = None

        if login_data is not None:
            user = find_user(login_data['data'], request.json['username'])
        else:
            error = 'Error getting data!'
            error_code = 500

        if error is None:
            if user is not None:
                if user['password'] == request.json['password']:
                    profile_data = local_data_get('profile')
                    user = find_user(profile_data['data'], request.json['username'])

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
