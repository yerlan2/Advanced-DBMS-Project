/*
Is the commentator of the post
that has a couple of pictures liked the post and
is he the follower of the author?
If yes output the name of the commentator.
*/

CREATE VIEW IF NOT EXISTS v_sixteenth
AS
SELECT DISTINCT(a.name)
FROM comments c, likes l, postimages pi, subscriptions s, accounts a
WHERE c.post_id = l.post_id AND c.account_id = l.account_id
AND c.post_id = pi.post_id
AND c.account_id = s.follower_id
AND c.account_id = a.id;

SELECT * FROM v_sixteenth;