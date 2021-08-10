import click
import json
import requests
from flask_scrypt import check_password_hash


urlLogin = 'https://api.jsonbin.io/v3/b/60ee82b3c1256a01cb6ec53e'
urlUser = 'https://api.jsonbin.io/v3/b/60ee8281c1256a01cb6ec524'
urlNote = 'https://api.jsonbin.io/v3/b/60ee82530cd33f7437c7f1e0'
urlProfile = 'https://api.jsonbin.io/v3/b/60fad285a263d14a297ac102'


def get_all(which):
    db = get_db(which)
    resp = get_data(**db)

    return_var = {
        'url_meta': db,
        'data': json.loads(resp)
    }

    return return_var


def get_db(whichdb):
    headers = {
        'X-Master-Key': '$2b$10$BZ5hdRth9T2taHpARhKJK.AwqV/cLWEYozpt2iMBbtZE5S0YFo97i'
    }
    if whichdb == 'login':
        url = urlLogin
    elif whichdb == 'user':
        url = urlUser
    elif whichdb == 'profile':
        url = urlProfile
    elif whichdb == 'note':
        url = urlNote

    db = {
        'url': url,
        'headers': headers
    }

    return db


def get_data(url, headers):
    req = requests.get(url + '/latest', headers=headers)

    return req.text


def update_data(url, headers, data):

    click.echo(f'meta-url: {url}, meta-headers: {headers}')
    click.echo(f'data: {data}')
    headers['X-Bin-Versioning'] = 'false'

    # req = requests.put(url, json=data, headers=headers)
    #
    # if req.status_code == 200:
    #     return '', 204
    # else:
    #     return {'errorMessage': 'error updating'}, 500
    return '', 204


def close_db(db, whichdb):
    if db is not None:
        if whichdb == 'login':
            db = 'loginDB'
        elif whichdb == 'user':
            db = 'userDB'
        else:
            db = 'noteDB'

    return db
