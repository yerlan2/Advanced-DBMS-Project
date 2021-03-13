/*
Find a post that is more than 3 years old and which has more than three comments and at least 
2 images and category is IT or music and which the author liked his own publication. List the output by comment 
amount in descending order.
*/

CREATE UNIQUE INDEX idx_categories_name 
ON categories (name);

CREATE VIEW v_fifth
AS 
SELECT p.id
FROM posts p
INNER JOIN comments cm ON p.id = cm.post_id
INNER JOIN categories cg ON p.category_id = cg.id
INNER JOIN postimages pm ON p.id = pm.post_id
INNER JOIN likes l ON p.account_id = l.account_id
GROUP BY p.id
HAVING (julianday('now') - julianday(p.created_date)) / 365 > 3
AND cg.name = "IT" OR "Music"
AND count(pm.post_id) >= 2
AND count(cm.id) > 3
ORDER BY count(cm.id) DESC;

SELECT * FROM v_fifth;