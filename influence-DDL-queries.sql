CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    image_id INTEGER
);
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    category_id INTEGER,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_date DATETIME DEFAULT current_timestamp,
    like_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    added_date DATETIME DEFAULT current_timestamp
);
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS likes (
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS subscriptions (
    follower_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS postimages (
    post_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL
);

