import functools
import json

from flask import (
    Blueprint, flash,  request, abort, jsonify
)
from api.db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')


def dict_from_row(row):
    return dict(zip(row.keys(), row))


@bp.route('/', methods=['GET'])
def get_users():
    response = get_db().execute('SELECT * from users').fetchall()

    if response is None:
        abort(404, "No users in database")

    users = [dict_from_row(row) for row in response]

    return {"users": users}


@bp.route('/', methods=['POST'])
def create_user():
    db = get_db()

    form = json.loads(request.json)
    error = None

    if not form.get("first_name") or not form.get("last_name") or not form.get("email"):
        error = "first name, last name, and email required"
        abort(400, error)

    if error is None:
        first_name = form['first_name']
        last_name = form['last_name']
        email = form['email']
        has_loan = False
        has_other_loan = False
        if form.get('has_loan'):
            has_loan = form['has_loan']
        if form.get('has_other_loan'):
            has_other_loan = form['has_other_loan']

        user = None
        try:
            db.execute(
                "INSERT INTO users (first_name, last_name, email, has_loan, has_other_loan) "
                "VALUES (?, ?, ?, ?, ?)"
                ,
                (first_name, last_name, email, has_loan, has_other_loan),
            )
            db.commit()

            user = db.execute("SELECT * from users WHERE email=?", (email,)).fetchone()
        except db.IntegrityError:
            error = f"Email {email} already exists"
            abort(400, error)

    user = dict_from_row(user)
    return {"user": user}


@bp.route('/<int:u_id>', methods=['GET'])
def get_user(u_id):
    response = get_db().execute('SELECT * FROM users WHERE id = ?', (u_id,)).fetchone()
    if not response:
        abort(404, "user does not exist")

    user = dict_from_row(response)
    return {"user": user}


@bp.route('/<int:u_id>', methods=['PUT', 'PATCH'])
def put_user(u_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (u_id,)).fetchone()
    values = ()
    if not user:
        abort(404, "user does not exist")

    statement = "UPDATE users SET"

    form = json.loads(request.json)

    for k, v in form.items():
        statement += f" {k} = ?,"
        values += (v,)

    statement = statement[:-1]
    statement += " WHERE id = ?"
    values += (u_id,)

    db.execute(statement, values)
    db.commit()

    user = db.execute("SELECT * FROM users WHERE id = ?", (u_id,)).fetchone()
    user = dict_from_row(user)
    return {"user": user}


@bp.route('/<int:u_id>', methods=['DELETE'])
def delete_user(u_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (u_id,)).fetchone()
    if not user:
        abort(404, "this user does not exist")

    db.execute("DELETE from users WHERE id = ?", (u_id,))

    return jsonify(True)
