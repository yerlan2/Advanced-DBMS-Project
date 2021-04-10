/*
Can a owner of posts see a owner of a like?
Displays Post ID and a name of a owner of a like. For example: Posts from Account#03880's posts.
*/

CREATE VIEW IF NOT EXISTS v_sixth
AS 
SELECT l.post_id 'Post ID', a.name 'Owner of a like'
FROM likes l, accounts a 
WHERE l.account_id = a.id
AND l.post_id IN (
    SELECT p.id 
    FROM posts p, accounts a 
    WHERE p.account_id = a.id 
    AND a.name = 'Account#03880'
);

SELECT * FROM v_sixth;
