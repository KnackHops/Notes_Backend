import click
from datetime import date
# for checking
# from flask_scrypt import (
#     generate_random_salt, generate_password_hash, check_password_hash
# )


def get_db_models(user=False, login=False, profile=False, note=False):
    from flaskr import _sq
    _db = []

    if user:
        from flaskr import _User
        _db.append(_User)

    if login:
        from flaskr import _Login
        _db.append(_Login)

    if profile:
        from flaskr import _ProfileUpdate
        _db.append(_ProfileUpdate)

    if note:
        from flaskr import _Note
        _db.append(_Note)

    return _sq, _db


def init_db(db):
    class User(db.Model):
        __tablename__ = 'user'

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.VARCHAR(155), unique=True, nullable=False)
        email = db.Column(db.VARCHAR(155), unique=True, nullable=False)
        mobile = db.Column(db.VARCHAR(12), nullable=True)
        pfp = db.Column(db.Text, default="default")
        nickname = db.Column(db.VARCHAR(15), nullable=True)

        login = db.relationship('Login',
                                lazy=True,
                                backref=db.backref('user', lazy=True),
                                uselist=False,
                                foreign_keys='Login.userid')
        login_username = db.relationship('Login', foreign_keys='Login.username', uselist=False)
        profile_update = db.relationship('ProfileUpdate',
                                         lazy=True,
                                         backref=db.backref('user', lazy=True),
                                         uselist=False)
        note = db.relationship('Note',
                               lazy=False,
                               backref=db.backref('user', lazy=False))

        def __repr__(self):
            return '<User %r>' % self.username

    class Login(db.Model):
        __tablename__ = 'login'

        userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
        username = db.Column(db.VARCHAR(155), db.ForeignKey('user.username'), nullable=False)
        password = db.Column(db.LargeBinary, nullable=False)
        salt = db.Column(db.LargeBinary, nullable=False)

        def __repr__(self):
            return '<Login %r>' % self.username

    class ProfileUpdate(db.Model):
        __tablename__ = 'profile_update'

        userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
        pfp_last = db.Column(db.DATE, default=date.today())
        nick_last = db.Column(db.DATE, default=date.today())

        def __repr__(self):
            return '<ProfileUpdate %r>' % self.userid

    class Note(db.Model):
        __tablename__ = 'note'

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.VARCHAR(155), db.ForeignKey('user.username'), nullable=False)
        title = db.Column(db.Text, nullable=True)
        body = db.Column(db.Text, nullable=True)
        editable = db.Column(db.BOOLEAN, default=False)
        locked = db.Column(db.BOOLEAN, default=False)
        locked_password = db.Column(db.VARCHAR(4), nullable=True)
        date_created = db.Column(db.DATE, default=date.today())
        last_updated = db.Column(db.DATE, nullable=True)

        def __repr__(self):
            return '<Note %r>' % self.userid

    return User, Login, ProfileUpdate, Note

# for checking
# def add_test():
#     sq, [User, Login, ProfileUpdate] = get_db_models(user=True, login=True, profile=True)
#
#     new_user = User(username='affafu', email='himalosc@gmail.com')
#     salt = generate_random_salt(128)
#     password = generate_password_hash('few', salt)
#     new_login = Login(username=new_user.username, password=password, salt=salt)
#     new_profile = ProfileUpdate()
#     new_user.login = new_login
#     new_user.profile_update = new_profile
#     sq.session.add(new_user)
#
#     try:
#         sq.session.commit()
#     except sqlalchemy.exc.IntegrityError as e:
#         orig = str(e.orig)
#
#         if 'UNIQUE' in orig:
#             if 'email' in orig:
#                 pass
#             else:
#                 pass
#
#
# def query_test():
#     sq, [Note] = get_db_models(note=True)
#
#     try:
#         note = Note.query.filter_by(userid=1).all()
#         if note:
#             click.echo("work?")
#         else:
#             click.echo("nah")
#     except:
#         click.echo('err')


def update_test():
    pass
