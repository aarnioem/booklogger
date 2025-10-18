CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    title TEXT,
    author TEXT,
    status_id INTEGER REFERENCES reading_status(id),
    rating INTEGER,
    review TEXT
);

CREATE TABLE reading_status (
    id INTEGER PRIMARY KEY,
    status TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    log_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE covers (
    id INTEGER PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    cover BLOB
);

CREATE INDEX idx_comments_user_id ON comments(user_id);