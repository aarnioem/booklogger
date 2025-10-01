from flask import abort, session
from werkzeug.security import check_password_hash

import db
from logs import get_log_user_id

def create_account(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def login(username, password):
    sql = "SELECT password_hash, id FROM users WHERE username = ?"
    query = db.query(sql, [username])

    if not query:
        return None

    password_hash = query[0]["password_hash"]
    user_id = query[0]["id"]

    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_users():
    sql = "SELECT username, id FROM users"
    result = db.query(sql, [])
    return result

def get_user(user_id):
    sql = "SELECT username, id FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0]

def check_permission(user_id, log_id):
    log_user_id = get_log_user_id(log_id)
    if log_user_id["user_id"] != user_id:
        abort(403)

def check_login():
    if "user_id" not in session:
        abort(401)
