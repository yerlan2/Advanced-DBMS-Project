-- SELECT author_id 
-- FROM subscriptions
-- WHERE follower_id=7500
-- ;

SELECT a.id, a.name, a.email, a.password, a.image_id
FROM subscriptions s, accounts a
WHERE s.author_id = a.id
AND s.follower_id=7500
ORDER BY a.id DESC
;
