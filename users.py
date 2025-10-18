from secrets import token_hex
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
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = token_hex(16)
        return True
    return None

def get_users():
    sql = "SELECT username, id FROM users"
    result = db.query(sql, [])
    return result

def get_user(user_id):
    sql = "SELECT username, id, created_at FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    if not result:
        abort(404)
    return result[0]

def get_user_stats(user_id):
    sql = """SELECT users.id AS user_id,
                    users.username,
                    users.created_at,
                    COUNT(DISTINCT CASE WHEN reading_status.status = 'want-to-read' THEN books.id END) AS want_to_read_count,
                    COUNT(DISTINCT CASE WHEN reading_status.status = 'reading' THEN books.id END) AS reading_count,
                    COUNT(DISTINCT CASE WHEN reading_status.status = 'read' THEN books.id END) AS read_count,
                    COUNT(DISTINCT CASE WHEN reading_status.status = 'dropped' THEN books.id END) AS dropped_count,
                    COUNT(DISTINCT CASE WHEN reading_status.status = 'on-hold' THEN books.id END) AS on_hold_count,
                    COUNT(DISTINCT books.id) AS total_logs,
                    COUNT(DISTINCT comments.id) AS total_comments
            FROM users
            LEFT JOIN books ON users.id = books.user_id
            LEFT JOIN reading_status ON books.status_id = reading_status.id
            LEFT JOIN comments ON users.id = comments.user_id
            WHERE users.id = ?"""

    result = db.query(sql, [user_id])

    return result[0]


def check_permission(user_id, log_id):
    log_user_id = get_log_user_id(log_id)
    if log_user_id["user_id"] != user_id:
        abort(403)

def check_login():
    if "user_id" not in session:
        abort(401)

def check_csrf(csrf):
    if csrf != session["csrf_token"]:
        abort(403)
