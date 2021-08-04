import click
from flask import (
    Blueprint, request, make_response
)
from flaskr.db import (
    get_all,
)

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/fetch-all', methods=('GET', 'POST'))
def fetch_all():
    if request.method == 'POST':
        note_db = get_all('note')
        error = None
        errno = None

        users_note = []

        if 'data' not in note_db:
            error = 'error fetching notes'
            errno = 500

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

        return make_response(({'errorMessage': error}, errno))


@bp.route('/save-note', methods=('GET', 'POST'))
def save_note():
    if request.method == 'POST':
        note_db = get_all('note')
        error = None
        errno = None

        if 'data' not in note_db:
            error = 'error fetching data!'
            errno = 500

        if error is None:
            note_data = note_db['data']['record']
            note_data.append(request.json['note'])

            # put the update method here
            # click.echo(note_data)

            new_note_data = []
            for note in note_data:
                if note['user'] == request.json['note']['user']:
                    new_note_data.append(note)

            return make_response(({'note': new_note_data}, 200))
        else:
            return make_response(({'errorMessage': error}, errno))


@bp.route('/edit_note', methods=('GET', 'POST'))
def edit_note():
    if request.method == 'POST':
        note_db = get_all('note')
        error = None
        errno = None

        if 'data' not in note_db:
            error = 'error fetching data!'
            errno = 500

        if error is None:
            note_data = note_db['data']['record']
            new_note_data = []
            for note in note_data:
                new_note = note
                if note['user'] == request.json['note']['user']:
                    if note['id'] == request.json['note']['id']:
                        new_note = request.json['note']

                new_note_data.append(new_note)
            # put the update method here

            return make_response(({'note': new_note_data}, 200))
        else:
            return make_response(({'errorMessage': error}, errno))


@bp.route('/delete-note', methods=('GET', 'POST'))
def delete_note():
    if request.method == 'POST':
        note_db = get_all('note')
        error = None
        errno = None

        if 'data' not in note_db:
            error = 'error fetching data!'
            errno = 500

        if error is None:
            note_data = note_db['data']['record']

            new_note_data = []
            for note in note_data:
                if note['user'] == request.json['note']['user']:
                    if not note['id'] == request.json['note']['id']:
                        new_note_data.append(note)

            return make_response(({'note': new_note_data}, 200))

        else:
            return make_response(({'errorMessage': error}, errno))


@bp.after_request
def after_request_func(response):
    response.headers['Content-Type'] = 'application/json'
    return response
