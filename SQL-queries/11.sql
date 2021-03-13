/*
Display account name, post number and average like number for each account with more than 5 followers, if that account has an post.
*/

CREATE VIEW IF NOT EXISTS v_eleventh
AS 
select a.name 'Account name', count(p.id) 'Post number', avg(p.like_count) 'Post average like number' 
from posts p, accounts a  
where p.account_id = a.id
group by p.account_id 
having p.account_id in (
    select author_id 
    from subscriptions
    group by author_id
    having count(follower_id) > 5
);

SELECT * FROM v_eleventh;
