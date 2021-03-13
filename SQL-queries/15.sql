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
  FROM comments c, posts p, likes l, subscriptions s, accounts a, postimages pi
 WHERE c.post_id = p.id
   AND c.account_id = a.id
   AND c.post_id = pi.post_id
   AND c.post_id = l.post_id
   AND c.account_id = l.account_id
   AND s.follower_id = c.account_id
   AND s.author_id = p.account_id
   AND p.title = 'Golden Park'
   AND pi.image_id != NULL
   AND l.account_id != NULL;