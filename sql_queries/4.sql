/*
Find the name of the accounts and the number of their subscribers who has an avatar image and has at least one subscriber, and that
is the author of the post, from the category science and in the title of which there is the word "white". List the output by follower 
amount in descending order.
*/

CREATE INDEX idx_posts_title 
ON posts (title);

CREATE UNIQUE INDEX idx_categories_name 
ON categories (name);

CREATE VIEW v_fourth
AS 
Select a.name, count(s.author_id) follower_amount
FROM accounts a
INNER JOIN images i ON a.image_id = i.id
INNER JOIN subscriptions s ON a.id = s.author_id
INNER JOIN posts p ON a.id = p.account_id 
INNER JOIN categories c ON p.category_id = c.id
GROUP BY a.name
HAVING follower_amount > 0
AND p.title LIKE '%white%'
AND c.name = "Science"
ORDER BY follower_amount DESC;

SELECT * FROM v_fourth;
