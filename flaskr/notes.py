import click
from flask import (
    Blueprint, request, make_response
)
from flaskr.db import (
    get_all,
)
from flask_cors import (
    CORS,
)
from flaskr.db import (
    update_data,
)

bp = Blueprint('notes', __name__)
CORS(bp, origins='http://127.0.0.1:5500/')


@bp.route('/fetch-all', methods=('GET', 'POST'))
def fetch_all():
    if request.method == 'POST':
        note_db = get_all('note')
        error = None
        error_code = None

        users_note = []

        if 'data' not in note_db:
            error = 'error fetching notes'
            error_code = 500

        if error is None:
            note_data = note_db['data']['record']
            for note in note_data:
                if request.json['user'] == note['user']:
                    users_note.append(note)

            if error is None:
                if len(users_note) == 0:
                    resp = make_response(({'note': 'None'}, 200))
                else:
                    resp = make_response(({'note': users_note}, 200))

                return resp

        return {'errorMessage': error}, error_code


@bp.route('/save', methods=('GET', 'POST'))
def save_note():
    if request.method == 'POST':
        note_db = get_all('note')
        error = None
        error_code = None

        if 'data' not in note_db:
            error = 'error fetching data!'
            error_code = 500

        if error is None:
            note_data = note_db['data']['record']
            note_meta = note_db['url_meta']
            new_note_data = []
            id = None
            for note in note_data:
                if note['user'] == request.json['user']:
                    if id is None:
                        id = note['id']
                    else:
                        if note['id'] > id:
                            id = note['id']

                new_note_data.append(note)

            if id is None:
                id = 0

            new_note = request.json['note']
            new_note['id'] = id

            new_note_data.append(new_note)

            update_data(**note_meta, data=new_note_data)

            return make_response(({'note': new_note_data}, 200))
        else:
            return {'errorMessage': error}, error_code


def actual_edit():
    note_db = get_all('note')
    error = None
    error_code = None

    if 'data' not in note_db:
        error = 'error fetching data!'
        error_code = 500

    if error is None:
        note_data = note_db['data']['record']
        new_note_data = []
        for note in note_data:
            new_note = note
            if note['user'] == request.json['note']['user']:
                if note['id'] == request.json['note']['id']:
                    if not new_note['title'] == request.json['note']['title']:
                        new_note['title'] = request.json['note']['title']
                    if not new_note['body'] == request.json['note']['body']:
                        new_note['body'] = request.json['note']['body']

                    new_note['lastUpdated'] = request.json['note']['lastUpdated']

            new_note_data.append(new_note)
        # put the update method here

        return make_response(({'note': new_note_data}, 200))
    else:
        return {'errorMessage': error}, error_code


def actual_edit_locked():
    return 'yo'


@bp.route('/edit', methods=('GET', 'PUT'))
def edit_note():
    if request.method == 'PUT':
        resp = actual_edit()
        return resp


@bp.route('/editablelocked', methods=('GET', 'PUT'))
def editable_locked():
    if request.method == 'PUT':
        resp = actual_edit_locked()
        return resp


@bp.route('/delete', methods=('GET', 'POST'))
def delete_note():
    if request.method == 'POST':
        note_db = get_all('note')
        error = None
        error_code = None

        if 'data' not in note_db:
            error = 'error fetching data!'
            error_code = 500

        if error is None:
            note_data = note_db['data']['record']

            new_note_data = []
            for note in note_data:
                if note['user'] == request.json['note']['user']:
                    if not note['id'] == request.json['note']['id']:
                        new_note_data.append(note)

            return make_response(({'note': new_note_data}, 200))

        else:
            return {'errorMessage': error}, error_code


@bp.route('/')
def index():
    return make_response(({"ya": "hallo"}, 200))


@bp.after_request
def after_request_func(response):
    response.headers['Content-Type'] = 'application/json'
    return response