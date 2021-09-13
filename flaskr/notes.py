from datetime import date
import werkzeug.exceptions
from flask import (
    Blueprint, request, make_response
)
from flaskr.db import get_db_models
from flask_cors import (
    CORS,
)

bp = Blueprint('notes', __name__)
CORS(bp, origins='*')


@bp.route('/fetch-all')
def fetch_all():
    if request.method == 'GET':
        sq, [Note] = get_db_models(note=True)
        error = None
        error_code = None

        if not sq or not Note:
            error_code = 500

        if not error_code:
            try:
                _notes = Note.query.filter_by(username=str(request.args.get('username'))).all()

                if _notes:
                    notes = []
                    for note in _notes:
                        date_created = date_extract(note.date_created)
                        last_updated = None
                        if note.last_updated:
                            last_updated = date_extract(note.last_updated)

                        notes.append({
                            'id': note.id,
                            'title': note.title,
                            'body': note.body,
                            'editable': note.editable,
                            'locked': note.locked,
                            'locked_password': note.locked_password,
                            'username': note.username,
                            'date_created': date_created,
                            'last_updated': last_updated
                        })

                    sq.session.close()
                    return make_response(({'notes': notes}, 200))
                else:
                    sq.session.close()
                    return make_response(({'notes': None}, 200))
            except:
                error_code = 500

        sq.session.close()
        return before_return(error_code, error)


@bp.route('/save-note', methods=('GET', 'POST'))
def save_note():
    if request.method == 'POST':
        sq, [User, Note] = get_db_models(user=True, note=True)
        error = None
        error_code = None

        if not sq or not Note:
            error_code = 500

        if not error_code:
            try:
                user = User.query.filter_by(
                    username=str(request.json['username'])).first_or_404(description='User does not exist!')

                new_note = Note(
                    title=request.json['title'],
                    body=request.json['body'],
                    editable=request.json['editable'],
                    locked=request.json['locked'],
                    locked_password=request.json['locked_password'],
                    username=user.username
                )

                sq.session.add(new_note)
                sq.session.commit()

                date_created = date_extract(new_note.date_created)

                note = {
                    'id': new_note.id,
                    'username': new_note.username,
                    'title': new_note.title,
                    'body': new_note.body,
                    'editable': new_note.editable,
                    'locked': new_note.locked,
                    'locked_password': new_note.locked_password,
                    'date_created': date_created,
                    'last_updated': new_note.last_updated
                }

                sq.session.close()
                return make_response((note, 200))
            except werkzeug.exceptions.NotFound as e:
                error_code = 404
                error = e.description

        sq.session.close()
        return before_return(error_code, error)


@bp.route('/edit', methods=('GET', 'PUT'))
def edit():
    if request.method == 'PUT':
        sq, [Note] = get_db_models(note=True)
        error_code = None
        error = None

        if not sq or not Note:
            error_code = 500

        if not error_code:
            try:
                note = Note.query.filter_by(
                    id=request.json['id'],
                    username=request.json['username']).first_or_404(description="Note doesn't exists")

                if 'title' in request.json:
                    note.title = request.json['title']
                if 'body' in request.json:
                    note.body = request.json['body']
                note.last_updated = date.today()

                sq.session.commit()
                sq.session.close()
                return '', 204
            except werkzeug.exceptions.NotFound as e:
                error_code = 404
                error = e.description

        sq.session.close()
        return before_return(error_code, error)


@bp.route('/update-edit-lock', methods=('GET', 'PUT'))
def update_edit_lock():
    if request.method == 'PUT':
        sq, [Note] = get_db_models(note=True)
        error_code = None
        error = None

        if not sq or not Note:
            error_code = 500

        if not error_code:
            try:
                note = Note.query.filter_by(
                    id=request.json['id'],
                    username=request.json['username']).first_or_404(description="Note doesn't exists")

                if note.locked == request.json['locked'] and note.locked_password == request.json['locked_password'] and note.editable == request.json['editable']:
                    error_code = 400
                    error = 'No change detected'
                else:
                    if not note.locked == request.json['locked']:
                        note.locked = request.json['locked']
                    if not note.locked_password == request.json['locked_password']:
                        locked_password = request.json['locked_password']
                        if note.locked:
                            if locked_password:
                                if len(request.json['locked_password']) == 4:
                                    note.locked_password = locked_password
                                else:
                                    raise Exception('locked_password is not 4 characters')
                            else:
                                raise Exception('locked_password is empty')
                        else:
                            locked_password = None
                            note.locked_password = locked_password
                    if not note.editable == request.json['editable']:
                        note.editable = request.json['editable']

                    sq.session.commit()
                    sq.session.close()
                    return '', 204
            except werkzeug.exceptions.NotFound as e:
                error_code = 404
                error = e.description
            except Exception as e:
                error_code = 400
                error = repr(e)
            except:
                error_code = 500

        sq.session.close()
        return before_return(error_code, error)


@bp.route('/delete', methods=('GET', 'DELETE'))
def delete():
    if request.method == 'DELETE':
        sq, [Note] = get_db_models(note=True)
        error_code = None
        error = None

        if not sq or not Note:
            error_code = 500

        if not error_code:
            try:
                note = Note.query.filter_by(
                    id=request.args.get('id'),
                    username=request.args.get('username')).first_or_404(description='Note not found!')

                sq.session.delete(note)
                sq.session.commit()
                sq.session.close()
                return '', 204
            except werkzeug.exceptions.NotFound as e:
                error_code = 404
                error = e.description
            except:
                error_code = 500

        return before_return(error_code, error)


@bp.after_request
def after_request_func(response):
    response.headers['Content-Type'] = 'application/json'
    return response


def before_return(error_code, error):
    if error_code:
        if error_code == 500:
            error = 'Internal Server Error'
        return {'errorMessage': error}, error_code


def date_extract(_date):
    date_extracted = _date.timetuple()

    return {
        'year': date_extracted[0],
        'month': date_extracted[1],
        'day': date_extracted[2]
    }
