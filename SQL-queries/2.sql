/*
List authors by their popularity(amount of followers, likes and comments)
*/

CREATE VIEW v_second
AS 
SELECT a.name
FROM accounts a
INNER JOIN subscriptions s ON s.author_id = a.id
INNER JOIN posts p ON p.account_id = a.id
INNER JOIN likes l ON l.post_id = p.id
INNER JOIN comments cm ON cm.post_id = p.id
GROUP BY a.id
ORDER BY count(s.author_id) and count(l.post_id) and count(cm.post_id) DESC;

SELECT * FROM v_second;
