INSERT INTO app.app_coupon
SELECT
NULL
,'a'
,s.userid
,s.htmlid
,500*(FLOOR(s.visit/500)-FLOOR((IFNULL(c.condi,0)+0)/500)) AS c
,20*(FLOOR(s.visit/500)-FLOOR((IFNULL(c.condi,0)+0)/500)) AS a
,NOW()
,DATE_ADD(NOW(),INTERVAL 14 DAY)
,'1'
FROM app.app_sharesite s
LEFT JOIN app.app_coupon c
ON s.htmlid = c.htmlid
AND c.coupontype = 'a'
WHERE FLOOR(s.visit/500) > FLOOR((IFNULL(c.condi,0)+0)/500);

INSERT INTO app.app_coupon
SELECT
NULL
,'b'
,s.userid
,s.htmlid
,20*(FLOOR(s.good/20)-FLOOR((IFNULL(c.condi,0)+0)/20)) AS c
,1*(FLOOR(s.good/20)-FLOOR((IFNULL(c.condi,0)+0)/20)) AS a
,NOW()
,DATE_ADD(NOW(),INTERVAL 7 DAY)
,'1'
FROM app.app_sharesite s
LEFT JOIN app.app_coupon c
ON s.htmlid = c.htmlid
AND c.coupontype = 'b'
WHERE FLOOR(s.good/20) > FLOOR((IFNULL(c.condi,0)+0)/20)
AND s.sharetype = 'article';

UPDATE app.app_coupon SET usable = '0'
WHERE NOW() > enddt;