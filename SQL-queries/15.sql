/*
Is the commentator of the post, which is called "Golden Park",
and has a couple of pictures, liked the post and
is he the follower of the author?
If yes output the name of the commentator.
*/

CREATE INDEX IF NOT EXISTS idx_post_title
ON posts(title);

CREATE VIEW IF NOT EXISTS v_sixteenth
AS
SELECT a.name
  FROM subscriptions s, posts p, comments c, likes l, accounts a, images i
 WHERE a.id = s.follower_id AND p.account_id = s.author_id
   AND c.post_id = p.id
   AND c.post_id = l.post_id AND c.account_id = l.account_id
   AND c.account_id = a.id
   AND a.image_id = i.id
   AND a.name = 'Golden Park'
   AND p.id = 1317;