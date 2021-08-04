import requests
from flask import (
    Blueprint, request, make_response
)
import click
from flaskr.db import (
    update_data, get_all
)
from flaskr.static.constant_var import HASH_FORMAT
from werkzeug.security import (
    generate_password_hash, check_password_hash
)

bp = Blueprint('user', __name__, url_prefix='/user')


def find_user(data, username):
    found = None
    for user in data['record']:
        if user['username'] == username:
            found = user
    return found


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login_db = get_all('login')
        error = None
        error_code = None
        user = None

        # click.echo(login_data['data']['record'])
        if login_db is not None:
            user = find_user(login_db['data'], request.json['login_data']['username'])
        else:
            error = 'Error getting data!'
            error_code = 500

        if error is None:
            if user is None:
                user_db = get_all('user')
                profile_db = get_all('profile')
                # three data are passed as request for register
                # three of which are named as:
                #   login_data
                #   user_data
                #   profile_data
                # the same name for the variables each of the database pulled
                list_db_metadata = [
                    login_db['url_meta'],
                    user_db['url_meta'],
                    profile_db['url_meta']
                ]
                list_db = [
                    login_db['data']['record'],
                    user_db['data']['record'],
                    profile_db['data']['record']
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

                    oldpass = request.json[list_request_var[x]]['password']

                    newuser = request.json[list_request_var[x]]
                    if x == 0:
                        newhash = generate_password_hash(password=oldpass, salt_length=16)
                        newuser['salt'] = newhash[20:38]
                        newuser['password'] = newhash[38:]

                    list_db[x].append(newuser)
                    click.echo(list_db[x])

                    response_update.append(
                        # this will register user
                        update_data(**each_url, data=list_db[x])
                    )
                    x = x + 1

                for eachResp in response_update:
                    if not eachResp:
                        error = 'error accessing database'
                        error_code = 500
                        # reset the changes done by removing the last item

                if not error:
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
        login_db = get_all('login')
        error = None
        error_code = None
        user = None

        if login_db is not None:
            user = find_user(login_db['data'], request.json['username'])
        else:
            error = 'Error getting data!'
            error_code = 500

        if error is None:
            if user is not None:
                newhash = f'{HASH_FORMAT}{user["salt"]}{user["password"]}'
                if check_password_hash(newhash, request.json['password']):
                    profile_data = get_all('profile')
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


@bp.route('/profilesave', methods=('GET', 'POST'))
def profile_save():
    if request.method == 'POST':
        user_db = get_all('user')
        user_data = user_db['data']['record']
        user_meta = user_db['url_meta']
        profile_db = get_all('profile')
        profile_data = profile_db['data']['record']
        profile_meta = profile_db['url_meta']

        new_user = []

        for user in user_data:
            user_update = user
            if user['username'] == request.json['username']:
                if 'pfp' in request.json:
                    user_update['pfp'] = request.json['pfp']
                if 'nickname' in request.json:
                    user_update['nickname'] = request.json['nickname']
                if 'mobile' in request.json:
                    user_update['mobile'] = request.json['mobile']

            new_user.append(user_update)

        new_profile = []

        for profile in profile_data:
            profile_update = profile
            if profile['username'] == request.json['username']:
                if 'pfpLast' in request.json:
                    profile_update['pfpLast'] = request.json['pfpLast']
                if 'nickLast' in request.json:
                    profile_update['nickLast'] = request.json['nickLast']

            new_profile.append(profile_update)

        update_data(**user_meta, data=new_user)
        update_data(**profile_meta, data=new_profile)

    return 'none'


@bp.after_request
def after_request_func(response):
    response.headers['Content-Type'] = 'application/json'
    return response


def update_db_password():
    pass
    # db = get_all('profile')
    # login_data = db['data']['record']

    # new_users = []
    # for user in login_data:
    #     # click.echo(f'{HASH_FORMAT}{user["password"][20:38]}{user["password"][38:]}')
    #     # click.echo(user['password'])
    #     new_user = {
    #         'username': user['username'],
    #         'password': user['password'][38:],
    #         'salt': user['password'][20:38]
    #     }
    #     new_users.append(new_user)

    # click.echo(new_users)
    # update_data(db['url_meta']['url'], db['url_meta']['headers'], new_users)
    # click.echo(db['url_meta']['headers'])
    # url = db['url_meta']['url'] + '/versions'
    # headers = db['url_meta']['headers']
    # headers['X-Preserve-Latest'] = 'true'
    # req = requests.delete(url, json=None, headers=headers)
