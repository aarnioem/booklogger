import db

def add_log(title, author, status_id, rating, review, user_id):
    sql = """ INSERT INTO books
              (user_id, title, author, status_id, rating, review)
              VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, title, author, status_id, rating, review])

def get_all_logs():
    sql = """SELECT books.id,
                    books.user_id,
                    books.title,
                    books.author,
                    books.status_id,
                    reading_status.status,
                    books.rating,
                    books.review,
                    users.username
            FROM books
            JOIN users ON books.user_id = users.id
            JOIN reading_status ON books.status_id = reading_status.id
            ORDER BY books.id DESC"""
    return db.query(sql, [])

def get_logs_by_user_id(user_id):
    sql = """SELECT books.id,
                    books.user_id,
                    books.title,
                    books.author,
                    books.status_id,
                    reading_status.status,
                    books.rating,
                    books.review
                    FROM books
                    JOIN reading_status ON books.status_id = reading_status.id
                    WHERE books.user_id = ?"""
    logs = db.query(sql, [user_id])
    return logs

def get_log_by_id(log_id):
    sql = """SELECT books.id,
                    books.user_id,
                    books.title,
                    books.author,
                    books.status_id,
                    reading_status.status,
                    books.rating,
                    books.review
                    FROM books
                    JOIN reading_status ON books.status_id = reading_status.id
                    WHERE books.id = ?"""
    log = db.query(sql, [log_id])
    return log[0]

def get_log_user_id(log_id):
    sql = "SELECT user_id FROM books WHERE id = ?"
    log = db.query(sql, [log_id])
    return log[0]

def update_log(status_id, rating, review, log_id):
    sql = "UPDATE books SET status_id = ?, rating = ?, review = ? WHERE id = ?"
    db.execute(sql, [status_id, rating, review, log_id])

def delete_log(log_id):
    sql = "DELETE FROM books WHERE id = ?"
    db.execute(sql, [log_id])

def search_by_title(query):
    sql = """SELECT books.id,
                    books.user_id,
                    books.title,
                    books.author,
                    books.status_id,
                    reading_status.status,
                    books.rating,
                    books.review,
                    users.username
            FROM books
            JOIN users ON books.user_id = users.id
            JOIN reading_status ON books.status_id = reading_status.id
            WHERE title LIKE ?"""
    return db.query(sql, ["%" + query + "%"])

def add_comment(log_id, user_id, content):
    sql = "INSERT INTO comments (log_id, user_id, content) VALUES (?, ?, ?)"
    db.execute(sql, [log_id, user_id, content])

def delete_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def comment_owner_id(comment_id):
    sql = "SELECT user_id FROM comments WHERE id = ?"
    result = db.query(sql, [comment_id])[0][0]

    if result:
        return result
    return None

def get_comments_by_log_id(log_id):
    sql = """SELECT comments.id,
                    comments.log_id,
                    comments.content,
                    comments.created_at,
                    users.username,
                    users.id as user_id
            FROM comments JOIN users ON comments.user_id = users.id
            WHERE comments.log_id = ?
            ORDER BY comments.created_at ASC"""
    return db.query(sql, [log_id])

def get_status_id(status):
    sql = "SELECT id FROM reading_status WHERE status = ?"
    result = db.query(sql, [status])
    if result:
        return result[0][0]
    return None
