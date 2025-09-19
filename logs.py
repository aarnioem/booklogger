import db

def add_log(title, author, status, rating, review, user_id):
    sql = "INSERT INTO books (user_id, title, author, status, rating, review) VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, title, author, status, rating, review])

def get_logs_by_id(user_id):
    sql = "SELECT * FROM books WHERE user_id = ?"
    logs = db.query(sql, [user_id])
    return logs