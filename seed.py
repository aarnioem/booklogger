import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM books")

user_count = 1000
log_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, log_count + 1):
    db.execute("""INSERT INTO books (user_id, title, author, status_id, rating, review)
                                  VALUES (?, ?, ?, ?, ?, ?)""",
               [random.randint(0, 999),
                "title" + str(i),
                "author" + str(i),
                random.randint(0, 4),
                random.randint(1, 10),
                random.randint(0, 40) * "Review! "])

for i in range(comment_count):
    db.execute("INSERT INTO comments (log_id, user_id, content) VALUES (?, ?, ?)",
               [random.randint(1, 10**5),
                random.randint(0, 999),
                random.randint(1, 20) * "comment! "])

db.commit()
db.close()
