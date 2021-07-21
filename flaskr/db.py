from flask import g
import requests
import json


urlLogin = 'https://api.jsonbin.io/v3/b/60ee82b3c1256a01cb6ec53e/latest'
urlUser = 'https://api.jsonbin.io/v3/b/60ee8281c1256a01cb6ec524/latest'
urlNote = 'https://api.jsonbin.io/v3/b/60ee82530cd33f7437c7f1e0/latest'


def get_db(whichdb):
    headers = {
        'X-Master-Key': '$2b$10$BZ5hdRth9T2taHpARhKJK.AwqV/cLWEYozpt2iMBbtZE5S0YFo97i'
    }
    if whichdb == 'login':
        db = requests.get(urlLogin, headers=headers)
    elif whichdb == 'user':
        db = requests.get(urlUser, headers=headers)
    else:
        db = requests.get(urlNote, headers=headers)

    return json.loads(db.text)


def close_db(db, whichdb):
    if db is not None:
        if whichdb == 'login':
            db = 'loginDB'
        elif whichdb == 'user':
            db = 'userDB'
        else:
            db = 'noteDB'

    return db
