import db

def add_log(title, author, status, rating, review, user_id):
    sql = """ INSERT INTO books
              (user_id, title, author, status, rating, review)
              VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, title, author, status, rating, review])

def get_all_logs():
    sql = """SELECT books.id,
                    books.user_id,
                    books.title,
                    books.author,
                    books.status,
                    books.rating,
                    books.review,
                    users.username
            FROM books JOIN users ON books.user_id = users.id
            ORDER BY books.id DESC"""
    return db.query(sql, [])

def get_logs_by_user_id(user_id):
    sql = "SELECT id, user_id, title, author, status, rating, review FROM books WHERE user_id = ?"
    logs = db.query(sql, [user_id])
    return logs

def get_log_by_id(log_id):
    sql = "SELECT id, user_id, title, author, status, rating, review FROM books WHERE id = ?"
    log = db.query(sql, [log_id])
    return log[0]

def get_log_user_id(log_id):
    sql = "SELECT user_id FROM books WHERE id = ?"
    log = db.query(sql, [log_id])
    return log[0]

def update_log(status, rating, review, log_id):
    sql = "UPDATE books SET status = ?, rating = ?, review = ? WHERE id = ?"
    db.execute(sql, [status, rating, review, log_id])

def delete_log(log_id):
    sql = "DELETE FROM books WHERE id = ?"
    db.execute(sql, [log_id])

def search_by_title(query):
    sql = """SELECT books.id,
                    books.user_id,
                    books.title,
                    books.author,
                    books.status,
                    books.rating,
                    books.review,
                    users.username
            FROM books JOIN users ON books.user_id = users.id
            WHERE title LIKE ?"""
    return db.query(sql, ["%" + query + "%"])

def add_comment(log_id, user_id, content):
    sql = "INSERT INTO comments (log_id, user_id, content) VALUES (?, ?, ?)"
    db.execute(sql, [log_id, user_id, content])

def get_comments_by_log_id(log_id):
    sql = """SELECT comments.id,
                    comments.log_id,
                    comments.content,
                    comments.created_at,
                    users.username,
                    users.id
            FROM comments JOIN users ON comments.user_id = users.id
            WHERE comments.log_id = ?
            ORDER BY comments.created_at ASC"""
    return db.query(sql, [log_id])
