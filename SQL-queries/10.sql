/*
Display the owner of the post and followers of the owner of the post with ID 6862, if the length of the category name is greater than 6.
*/

CREATE INDEX IF NOT EXISTS idx_categories_name 
ON categories(name);

CREATE VIEW IF NOT EXISTS v_tenth
AS 
SELECT a.name 'Post owner', (SELECT name FROM accounts WHERE id = s.author_id) 'Follower of a Post owner'
FROM posts p, categories c, accounts a, subscriptions s 
WHERE p.category_id = c.id 
AND p.account_id = a.id 
AND p.account_id = s.follower_id 
AND p.id = 6862 
AND length(c.name) > 6;

SELECT * FROM v_tenth;
