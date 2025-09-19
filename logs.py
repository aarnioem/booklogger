import db

def add_log(title, author, status, rating, review, user_id):
    sql = "INSERT INTO books (user_id, title, author, status, rating, review) VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, title, author, status, rating, review])

def get_logs_by_user_id(user_id):
    sql = "SELECT * FROM books WHERE user_id = ?"
    logs = db.query(sql, [user_id])
    return logs

def get_log_by_id(log_id):
    sql = "SELECT * FROM books WHERE id = ?"
    log = db.query(sql, [log_id])
    return log[0]

def update_log(status, rating, review, log_id):
    sql = "UPDATE books SET status = ?, rating = ?, review = ? WHERE id = ?"
    db.execute(sql, [status, rating, review, log_id])