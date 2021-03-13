/*
How many posts, which title starts with "A" and published no earlier than one week 
and have more than 35 likes, have an author, which have more than 10 followings
*/

CREATE INDEX idx_posts_title 
ON posts (title);

CREATE VIEW v_third
AS 
SELECT count(p.id)
FROM accounts a
INNER JOIN subscriptions s ON s.follower_id = a.id
INNER JOIN posts p ON p.account_id = a.id
INNER JOIN likes l ON l.post_id = p.id
GROUP BY a.id
HAVING count(s.follower_id) > 10
AND p.title LIKE 'A%'
AND (julianday('now') - julianday(p.created_date)) <= 7
AND count(l.post_id) > 35;

SELECT * FROM v_third;
