import functools

from flask import (
    Blueprint, flash,  request, abort
)
from api.db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=['GET'])
def get_users():
    users = get_db().execute('SELECT * from users').fetchall()

    if users is None:
        abort(404, "No users in database")

    return [user.to_json() for user in users]


@bp.route('/', methods=['POST'])
def create_user():
    db = get_db()

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    has_loan = request.form['has_loan']
    has_other_loan = request.form['has_other_loan']

    error = None

    if not first_name or not last_name:
        error = "first name and last name required"

    if error is None:
        try:
            db.execute(
                    "INSERT INTO users (first_name, last_name, email, has_loan, has_other_loan) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (first_name, last_name, email, has_loan, has_other_loan),
                )
            db.commit()
        except db.IntegrityError:
            error = f"Email {email} already exists"

        flash(error)

    return "User Created"


@bp.route('/<int:u_id>', methods=['GET'])
def get_user(u_id):
    user = get_db().execute('SELECT * FROM users WHERE id = ?', (u_id,))
    if not user:
        abort(404, "user does not exist")

    return user


@bp.route('/<int:u_id>', methods=['PUT', 'PATCH'])
def put_user(u_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (u_id,))
    values = ()
    if not user:
        abort(404, "user does not exist")

    statement = "UPDATE user SET"

    for k, v in request.form:
        statement += f"{k} = ?,"
        values.add(v)

    statement = statement[:-1]
    statement += " WHERE id = ?"
    values.add(u_id)

    db.execute(statement, values)
    db.commit()
    db.refresh(user)

    return user


@bp.route('/<int:u_id>', methods=['DELETE'])
def delete_user(u_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (u_id,))
    if not user:
        abort(404, "this user does not exist")

    db.execute("DELETE from users WHERE id = ?", (u_id,))

    return True
