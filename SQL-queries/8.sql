/*
Display a name_of_a_owner_of_a_like and ID of other posts that this owner of a like of a post with ID 2077 liked.
*/

CREATE VIEW IF NOT EXISTS v_eighth
AS 
SELECT a.name 'Name of a owner of a like', l.post_id 'Post ID' 
FROM accounts a, likes l 
WHERE a.id = l.account_id 
AND a.id IN (
    SELECT l.account_id 
    FROM posts p, likes l 
    WHERE p.id = l.post_id 
    AND p.id = 2077
) 
AND l.post_id <> 2077;

SELECT * FROM v_eighth;
