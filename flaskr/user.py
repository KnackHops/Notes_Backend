from flask import (
    Blueprint, request, make_response
)
import click
import json
from flaskr.db import (
    get_db, get_data, update_data
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
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

        click.echo(login_data['data']['record'])
        if login_data is not None:
            user = find_user(login_data['data'], request.json['login_data']['username'])
        else:
            error = 'Error getting data!'
            error_code = 500

        if error is None:
            if user is None:
                user_data = local_data_get('user')
                profile_data = local_data_get('profile')
                # three data are passed as request for register
                # three of which are named as:
                #   login_data
                #   user_data
                #   profile_data
                # the same name for the variables each of the database pulled
                list_db_metadata = [
                    login_data['url_meta'],
                    user_data['url_meta'],
                    profile_data['url_meta']
                ]
                list_db = [
                    login_data['data']['record'],
                    user_data['data']['record'],
                    profile_data['data']['record']
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

                    # click.echo(request.json[list_request_var[x]])

                    list_db[x].append(request.json[list_request_var[x]])

                    response_update.append(
                        update_data(**each_url, data=list_db[x])
                    )
                    x = x + 1

                for eachResp in response_update:
                    if not eachResp:
                        error = 'error accessing database'
                        error_code = 500
                        # reset the changes done by removing the last item

                if error is not None:
                    return 'register success!'

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


def update_db_password():
    pass
    # db = local_data_get('login')
    # login_data = db['data']['record']
    #
    # new_users = []
    #
    # for user in login_data:
    #     new_pass = generate_password_hash(user['password'], salt_length=16)
    #     new_users.append({
    #         'username': user['username'],
    #         'password': new_pass
    #     })

    # click.echo(login_data)
    # click.echo(new_users)
    # click.echo(db['url_meta'])

    # update_data(db['url_meta']['url'], db['url_meta']['headers'], new_users)
