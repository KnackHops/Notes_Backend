import requests
from flask import (
    Blueprint, request, make_response
)
import click
from flaskr.db import (
    update_data, get_all
)
from flaskr.static.constant_var import HASH_FORMAT
# from werkzeug.security import (
#     generate_password_hash, check_password_hash
# )
from flask_scrypt import (
    generate_random_salt, generate_password_hash, check_password_hash
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
        # print(request.json)

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

                for each_user in list_db[1]:
                    if each_user['email'] == request.json[list_request_var[1]]['email']:
                        error = 'Email already used before!'
                        error_code = 409

                if error is None:
                    x = 0
                    register_status = []

                    for each_url in list_db_metadata:
                        each_url['headers']['Content-Type'] = 'application/json'

                        newuser = request.json[list_request_var[x]]
                        if x == 0:
                            old_pass = request.json[list_request_var[x]]['password']
                            salt = generate_random_salt(128)
                            new_pass = generate_password_hash(old_pass, salt)
                            salt = salt.decode('ascii')
                            new_pass = new_pass.decode('ascii')

                            # newhash = generate_password_hash(password=oldpass, salt_length=16)
                            newuser['salt'] = salt
                            newuser['password'] = new_pass

                        list_db[x].append(newuser)

                        register_status.append(
                            # this will register user
                            update_data(**each_url, data=list_db[x])
                        )
                        x = x + 1

                    for status in register_status:
                        if 'errorMessage' in status:
                            error = 'error accessing database'
                            error_code = 500
                            # reset the changes done by removing the last item

                    if not error:
                        return 'register success!', 200
            else:
                error = 'User exist!'
                error_code = 302

        resp = {'errorMessage': error}, error_code

        return resp


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
                # newhash = f'{HASH_FORMAT}{user["salt"]}{user["password"]}'
                # if check_password_hash(newhash, request.json['password']):
                #     profile_data = get_all('profile')
                #     user = find_user(profile_data['data'], request.json['username'])
                #
                #     resp = make_response((user, 202))
                #     return resp
                # else:
                #     error = 'Wrong password!'
                if check_password_hash(request.json['password'], user['password'].encode('ascii'), user['salt'].encode('ascii')):
                    profile_db = get_all('profile')
                    user = find_user(profile_db['data'], request.json['username'])

                    resp = make_response((user, 200))
                    return resp
                else:
                    error = 'Wrong password!'
            else:
                error = 'User does not exist!'

        if error is not None and error_code is None:
            error_code = 404

        # resp = make_response(({'errorMessage': error}, error_code))

        return {'errorMessage': error}, 404


@bp.route('/profile-date-get', methods=('GET', 'POST'))
def profile_date_get():
    if request.method == 'POST':
        profile_db = get_all('profile')
        user = find_user(profile_db['data'], request.json['username'])

        if user is not None:
            return make_response((user, 200))
        else:
            return {'errorMessage': 'User does not exist!'}, 404


@bp.route('/profile-get', methods=('GET', 'POST'))
def profile_get():
    if request.method == 'POST':
        user_db = get_all('user')
        user = find_user(user_db['data'], request.json['username'])

        if user is not None:
            return make_response((user, 200))
        else:
            return {'errorMessage': 'User does not exist!'}, 404


@bp.route('/profile-save', methods=('GET', 'PUT'))
def profile_save():
    if request.method == 'PUT':
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

        update_status = []
        update_status.append(update_data(**user_meta, data=new_user))
        update_status.append(update_data(**profile_meta, data=new_profile))

        error = None
        for status in update_status:
            if 'errorMessage' in status:
                error = status['errorMessage']

        if error is None:
            return '', 204
        else:
            return {'errorMessage': error}, 500


@bp.after_request
def after_request_func(response):

    response.headers['Content-Type'] = 'application/json'

    return response


def update_db_password():
    pass
    db = get_all('login')
    # login_meta = db['url_meta']
    # login_data = db['data']['record']
    #
    # new_users = []
    # for user in login_data:
    #     if user['username'] == 'affafu':
    #         new_pass = 'affafuPass'
    #     else:
    #         new_pass = 'barryPass'
    #
    #     salt = generate_random_salt(128)
    #     new_pass = generate_password_hash(new_pass, salt)
    #     salt = salt.decode('ascii')
    #     new_pass = new_pass.decode('ascii')
    #
    #     new_user = {
    #         'username': user['username'],
    #         'password': new_pass,
    #         'salt': salt
    #     }
    #     new_users.append(new_user)
    #
    # click.echo(login_meta)
    # update_data(**login_meta, data=new_users)
    # click.echo(db['url_meta']['headers'])
    # url = db['url_meta']['url'] + '/versions'
    # headers = db['url_meta']['headers']
    # headers['X-Preserve-Latest'] = 'true'
    # req = requests.delete(url, json=None, headers=headers)
