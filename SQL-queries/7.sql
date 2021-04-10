/*
How do categories switch?
Display a name_of_a_post_owner and a post_ID of the accounts WHERE Account#06103 follows, as well as a post category - sport.
*/

CREATE INDEX IF NOT EXISTS idx_categories_name 
ON categories(name);

CREATE VIEW IF NOT EXISTS v_seventh
AS 
SELECT a.name 'Name of a owner of a post', p.id 'Post ID' 
FROM posts p, categories c, accounts a
WHERE p.category_id = c.id
AND p.account_id = a.id
AND p.account_id IN (
	SELECT s.author_id 
	FROM subscriptions s, accounts a 
	WHERE s.follower_id = a.id 
	AND a.name = 'Account#06103'
)
AND c.name = 'Sport';

SELECT * FROM v_seventh;
