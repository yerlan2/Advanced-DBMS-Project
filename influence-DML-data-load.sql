PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

.mode csv
.import ../data/accounts.csv accounts
.import ../data/posts.csv posts
.import ../data/comments.csv comments
.import ../data/categories.csv categories
.import ../data/images.csv images
.import ../data/likes.csv likes
.import ../data/subscriptions.csv subscriptions
.import ../data/postimages.csv postimages

COMMIT;

PRAGMA foreign_keys=on;