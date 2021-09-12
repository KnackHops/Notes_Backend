import sqlalchemy.exc
import werkzeug.exceptions
from datetime import date
from flask import (
    Blueprint, request, make_response
)
from flaskr.db import (
    get_db_models,
)
from flask_scrypt import (
    generate_random_salt, generate_password_hash, check_password_hash
)

bp = Blueprint('user', __name__, url_prefix='/user')


def find_user(data, userid=None, username=None):
    found = None
    for user in data['record']:
        if username is None:

            if user['userid'] == int(userid):
                found = user
        else:
            if user['username'] == username:
                found = user
    return found


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        sq, [User, Login, ProfileUpdate] = get_db_models(user=True, login=True, profile=True)
        error = None
        error_code = None

        if sq:
            for each in [User, Login, ProfileUpdate]:
                if not error_code:
                    if not each:
                        error_code = 500
        else:
            error_code = 500

        if not error_code:
            user_data = request.json['user_data']
            login_data = request.json['login_data']

            new_user = User(username=user_data['username'], email=user_data['email'])
            salt = generate_random_salt(128)
            password = generate_password_hash(login_data['password'], salt)
            new_login = Login(username=new_user.username, password=password, salt=salt)
            new_profile = ProfileUpdate()
            new_user.login = new_login
            new_user.profile_update = new_profile

            try:
                sq.session.add(new_user)
                sq.session.commit()
                sq.session.close()
                return '', 204
            except sqlalchemy.exc.IntegrityError as e:
                orig = str(e.orig)

                if 'UNIQUE' in orig:
                    if 'username' in orig:
                        error = 'username already exists!'
                    if 'email' in orig:
                        error = 'email already exists!'
                    error_code = 409
            except:
                error_code = 500

        sq.session.close()
        before_return(error_code, error)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        sq, [Login] = get_db_models(login=True)
        error = None
        error_code = None

        if not sq or not Login:
            error_code = 500

        if not error_code:
            try:
                user_login = Login.query.filter_by(username=request.json['username'])\
                    .first_or_404(description='User not found')

                if check_password_hash(request.json['password'], user_login.password, user_login.salt):

                    pfp_last = date_extract(user_login.user.profile_update.pfp_last)
                    nick_last = date_extract(user_login.user.profile_update.nick_last)

                    user = {
                        'userid': user_login.user.profile_update.userid,
                        'pfp_last': pfp_last, 'nick_last': nick_last
                    }

                    sq.session.close()
                    return make_response((user, 200))
                else:
                    error_code = 403
                    error = 'Password does not match!'
            except werkzeug.exceptions.NotFound:
                error_code = 404
                error = "User does not exist!"
            except:
                error_code = 500

        sq.session.close()
        return before_return(error_code, error)


@bp.route('/profile-date-get/')
def profile_date_get():
    if request.method == 'GET':
        sq, [Profile] = get_db_models(profile=True)
        error = None
        error_code = None

        if not sq or not Profile:
            error_code = 500

        if not error_code:
            userid = int(request.args.get('userid'))
            try:
                user_profile = Profile.query.filter_by(userid=userid).first_or_404(description='User does not exists!')

                pfp_last = date_extract(user_profile.pfp_last)
                nick_last = date_extract(user_profile.nick_last)

                user = {
                    'userid': userid,
                    'pfpLast': pfp_last, 'nickLast': nick_last
                }

                sq.session.close()
                return make_response((user, 200))
            except werkzeug.exceptions.NotFound as e:
                error_code = 404
                error = e.description
            except:
                error_code = 500

        sq.session.close()
        return before_return(error_code, error)


@bp.route('/user-get')
def user_get():
    if request.method == 'GET':
        sq, [User] = get_db_models(user=True)
        error_code = None
        error = None

        if not sq or not User:
            error_code = 500

        if not error_code:
            try:
                user_data = User.query.filter_by(id=int(request.args.get('userid')))\
                    .first_or_404(description='user does not exist')
                user = {
                    'username': user_data.username,
                    'nickname': user_data.nickname,
                    'email': user_data.email,
                    'mobile': user_data.mobile,
                    'pfp': user_data.pfp
                }
                sq.session.close()
                return make_response((user, 200))
            except werkzeug.exceptions.NotFound as e:
                error_code = 404
                error = e.description
            except:
                error_code = 500

        sq.session.close()
        return before_return(error_code, error)


@bp.route('/user-save', methods=('GET', 'POST'))
def user_save():
    if request.method == 'POST':
        sq, [User] = get_db_models(user=True)
        error_code = None
        error = None

        if not sq or not User:
            error_code = 500

        if not error_code:
            try:
                user = User.query.filter_by(id=request.json['userid']).first_or_404(description='User does not exists')

                if 'pfp' in request.json:
                    user.pfp = request.json['pfp']
                    user.profile_update.pfp_last = date.today()
                if 'nickname' in request.json:
                    nick_length = len(request.json['nickname'])
                    if 15 >= nick_length >= 4:
                        user.nickname = request.json['nickname']
                        user.profile_update.nick_last = date.today()
                    else:
                        error = 'nickname should be 15 maximum and 4 minimum'
                if 'mobile' in request.json:
                    mobile_length = len(request.json['mobile'])
                    if 13 >= mobile_length >= 11:
                        user.mobile = request.json['mobile']
                        user.profile_update.mobile_last = date.today()
                    else:
                        error = 'mobile number should be 13 maximum and 11 minimum'

                if error:
                    error_code = 406
                else:
                    sq.session.commit()
                    sq.session.close()
                    return '', 204
            except werkzeug.exceptions.NotFound as e:
                error_code = 404
                error = e.description
            except:
                error_code = 500

        sq.session.close()
        return before_return(error_code, error)


@bp.after_request
def after_request_func(response):

    response.headers['Content-Type'] = 'application/json'

    return response


def date_extract(_date):
    date_extracted = _date.timetuple()

    return {
        'year': date_extracted[0],
        'month': date_extracted[1],
        'day': date_extracted[2]
    }


def before_return(error_code, error):
    if error_code:
        if error_code == 500:
            error = 'Internal Server Error'
        return {'errorMessage': error}, error_code
