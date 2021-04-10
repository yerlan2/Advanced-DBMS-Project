/*
If I don't like a user, how can I unsubscribe from him?
*/

DELETE FROM subscriptions 
WHERE follower_id=1
AND author_id=10;

