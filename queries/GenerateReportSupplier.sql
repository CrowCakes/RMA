SELECT Supplier, COUNT(*) as Total, 
(COUNT(*) / (SELECT COUNT(*) FROM Entry WHERE DateReported >= %(start)s AND DateReported <= %(end)s)) * 100 AS Percentage
FROM Entry
WHERE DateReported >= %(start)s AND DateReported <= %(end)s 
GROUP BY Supplier