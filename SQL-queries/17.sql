/*
Find the name of the account that left comments in November
last year on the publication called "Player of the Year",
which is among those who put a like, there is a user named "Ivan"
*/

CREATE VIEW IF NOT EXISTS v_seventeenth
AS
SELECT a.name
  FROM accounts a, posts p, likes l
 WHERE 
       p.title = 'Player of the Year'
   AND (
       SELECT count(*)
         FROM comments c
        WHERE c.post_id = p.id
          AND c.added_date 
      BETWEEN '2020-11-01' AND '2020-11-30'
   ) > 0
   AND (
       SELECT count(*)
         FROM likes l1, accounts a1
        WHERE l1.account_id = a1.id
          AND a1.name = 'Ivan'
   ) > 0;

SELECT * FROM v_seventeenth;