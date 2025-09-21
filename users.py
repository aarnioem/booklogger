import db
from werkzeug.security import check_password_hash

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