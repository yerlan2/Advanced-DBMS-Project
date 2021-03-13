/*
Is the subscriber the author of a post that has more
than 30 likes, and the category name length is more than 4,
and the number of images of the post is more than one?
If yes, output subscriber name.
*/

CREATE VIEW IF NOT EXISTS v_sixteenth_posts
AS
SELECT like_count, c.name as category
  FROM posts p, categories c
 WHERE p.category_id = c.id
   AND length(c.name) > 4;

CREATE VIEW IF NOT EXISTS v_sixteenth_likers
AS
SELECT a.name as liker, c.name as category
  FROM likes l, posts p, categories c, accounts a
 WHERE l.post_id = p.id
   AND l.account_id = a.id
   AND p.category_id = c.id
   AND length(c.name) > 4;

SELECT * FROM v_sixteenth_posts;
SELECT * FROM v_sixteenth_likers;