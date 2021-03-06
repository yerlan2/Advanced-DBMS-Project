PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    image_id INT
);
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INT NOT NULL,
    category_id INT,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_date DATETIME DEFAULT current_timestamp,
    like_count INT DEFAULT 0,
    view_count INT DEFAULT 0
);
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INT NOT NULL,
    account_id INT NOT NULL,
    content TEXT NOT NULL,
    added_date DATETIME DEFAULT current_timestamp
);
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL
);
CREATE TABLE likes (
    post_id INT NOT NULL,
    account_id INT NOT NULL
);
CREATE TABLE subscriptions (
    account_id INT NOT NULL,
    following_id INT NOT NULL
);
CREATE TABLE postimages (
    post_id INT NOT NULL,
    image_id INT NOT NULL
);

.mode csv
.import ../data/accounts.csv accounts1
.import ../data/posts.csv posts1
.import ../data/comments.csv comments1
.import ../data/categories.csv categories1
.import ../data/images.csv images1
.import ../data/likes.csv likes1
.import ../data/subscriptions.csv subscriptions1
.import ../data/postimages.csv postimages1

INSERT INTO accounts SELECT * FROM accounts1;
INSERT INTO posts SELECT * FROM posts1;
INSERT INTO comments SELECT * FROM comments1;
INSERT INTO categories SELECT * FROM categories1;
INSERT INTO images SELECT * FROM images1;
INSERT INTO likes SELECT * FROM likes1;
INSERT INTO subscriptions SELECT * FROM subscriptions1;
INSERT INTO postimages SELECT * FROM postimages1;

DROP TABLE accounts1;
DROP TABLE posts1;
DROP TABLE comments1;
DROP TABLE categories1;
DROP TABLE images1;
DROP TABLE likes1;
DROP TABLE subscriptions1;
DROP TABLE postimages1;

COMMIT;

PRAGMA foreign_keys=on;