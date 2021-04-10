/*
How many likes does the post have,
with categories name’s length is more than 4,
and who are its owners?
*/

CREATE VIEW IF NOT EXISTS v_fourteenth_posts
AS
SELECT like_count, c.name as category
  FROM posts p, categories c
 WHERE p.category_id = c.id
   AND length(c.name) > 4;

CREATE VIEW IF NOT EXISTS v_fourteenth_likers
AS
SELECT a.name as liker, c.name as category
  FROM likes l, posts p, categories c, accounts a
 WHERE l.post_id = p.id
   AND l.account_id = a.id
   AND p.category_id = c.id
   AND length(c.name) > 4;

SELECT * FROM v_fourteenth_posts;
SELECT * FROM v_fourteenth_likers;