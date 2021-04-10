/*
How works the rendering of the post?
*/

-- post
CREATE VIEW IF NOT EXISTS v_twelfth_post
AS
SELECT title, content, c.name as category, created_date, like_count, view_count, a.name as author, i.path as avatar
  FROM posts p, categories c, accounts a, images i
 WHERE p.category_id = c.id
   AND p.account_id = a.id
   AND a.image_id = i.id
   AND p.id = 1;

-- post images
CREATE VIEW IF NOT EXISTS v_twelfth_post_images
AS
SELECT path as image
  FROM postimages pi, images i
 WHERE pi.image_id = i.id
   AND pi.post_id = 1;

-- post likes
CREATE VIEW IF NOT EXISTS v_twelfth_post_likes
AS
SELECT a.name as liker
  FROM likes l, accounts a
 WHERE l.account_id = a.id
   AND l.post_id = 3;

-- post comments
CREATE VIEW IF NOT EXISTS v_twelfth_post_comments
AS
SELECT c.content, a.name, c.added_date
  FROM comments c, accounts a
 WHERE c.account_id = a.id
   AND c.post_id = 1;

SELECT * FROM v_twelfth_post;
SELECT * FROM v_twelfth_post_images;
SELECT * FROM v_twelfth_post_likes;
SELECT * FROM v_twelfth_post_comments;