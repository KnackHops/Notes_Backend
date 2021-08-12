import json

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
                    resp = make_response(({'notes': 'None'}, 200))
                else:
                    resp = make_response(({'notes': users_note}, 200))

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
            return_note_data = []
            note_id = None

            for note in note_data:
                if note['user'] == request.json['user']:
                    return_note_data.append(note)
                    if note_id is None:
                        note_id = note['id']
                    else:
                        if note['id'] > note_id:
                            note_id = note['id']

                new_note_data.append(note)

            if note_id is None:
                note_id = 0

            new_note = request.json
            new_note['id'] = note_id
            new_note_data.append(new_note)
            return_note_data.append(new_note)
            update_data(**note_meta, data=new_note_data)

            return make_response(({'id': note_id}, 200))
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
        note_meta = note_db['url_meta']
        new_note_list = []

        for note in note_data:
            new_note = note
            if note['user'] == request.json['user']:
                if note['id'] == request.json['id']:
                    if not note['title'] == request.json['title']:
                        new_note['title'] = request.json['title']
                    if not note['body'] == request.json['body']:
                        new_note['body'] = request.json['note']['body']

                    new_note['lastUpdated'] = request.json['lastUpdated']

            new_note_list.append(new_note)

        update_status = update_data(**note_meta, data=new_note_list)

        if 'errorMessage' in update_status:
            error = update_status['errorMessage']
            error_code = update_status['error_code']
        else:
            return '', 204

    return {'errorMessage': error}, error_code


def actual_edit_locked():
    note_db = get_all('note')
    error = None
    error_code = None

    if 'data' not in note_db:
        error = 'error fetching data!'
        error_code = 500

    if error is not None:
        note_data = note_db['data']['record']
        note_meta = note_db['url_meta']

        new_note_list = []
        for note in note_data:
            new_note = note
            if note['user'] == request.method['user']:
                if note['id'] == request.method['id']:
                    if not note['locked'] == request.method['locked']:
                        new_note['locked'] = request.method['locked']
                        new_note['lockedPass'] = request.method['lockedPass']
                    if not note['editable'] == request.method['editable']:
                        new_note['editable'] = request.method['editable']

            new_note_list.append(new_note)

        update_status = update_data(**note_meta, data=new_note_list)

        if 'errorMessage' in update_status:
            error = update_status['errorMessage']
            error_code = update_status['error_code']
        else:
            return '', 204

    return {'errorMessage': error}, error_code


@bp.route('/edit', methods=('GET', 'PUT'))
def edit_note():
    if request.method == 'PUT':
        resp = actual_edit()
        return resp


@bp.route('/update-edit-lock', methods=('GET', 'PUT'))
def editable_locked():
    if request.method == 'PUT':
        resp = actual_edit_locked()
        return resp


@bp.route('/delete', methods=('GET', 'DELETE'))
def delete_note():
    if request.method == 'DELETE':
        note_db = get_all('note')
        id = int(request.args.get('id'))
        user = request.args.get('user')
        click.echo(type(id))
        click.echo(type(user))
        error = None
        error_code = None

        if 'data' not in note_db:
            error = 'error fetching data!'
            error_code = 500

        if error is None:
            note_data = note_db['data']['record']
            note_meta = note_db['url_meta']

            new_note_data = []
            for note in note_data:
                if not note['user'] == user:
                    new_note_data.append(note)
                else:
                    if not note['id'] == id:
                        new_note_data.append(note)

            update_data(**note_meta, data=new_note_data)

            return '', 204

        else:
            return {'errorMessage': error}, error_code


@bp.route('/')
def index():
    return make_response(({"ya": "hallo"}, 200))


@bp.after_request
def after_request_func(response):
    response.headers['Content-Type'] = 'application/json'
    return response

def update_note_cmd():
    pass
    # note_db = get_all('note')
    # note_meta = note_db['url_meta']
    # note_data = note_db['data']['record']
    #
    # new_note_list = []
    # for note in note_data:
    #     new_note = note
    #     new_note['body'] = json.dumps(new_note['body'])
    #     new_note_list.append(new_note)
    #
    # update_data(**note_meta, data=new_note_list)