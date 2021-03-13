/*
Find comments which have less than 10 words in content and where owner post's 
title starts with "M" letter and which was published more than 15,000 hours ago. 
*/

CREATE INDEX idx_posts_title 
ON posts (title);

CREATE VIEW v_first
AS 
SELECT cm.id
FROM comments cm
INNER JOIN posts p ON p.id = cm.post_id
WHERE (length(cm.content) - length(replace(cm.content, ' ', '')) + 1) < 10 
AND p.title LIKE 'm%'
AND (julianday('now') - julianday(p.created_date)) * 24 > 15000;

SELECT * FROM v_first;