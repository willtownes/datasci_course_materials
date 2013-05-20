--queries used for assignment2
--1a
select count(*) from frequency where docid='10398_txt_earn';
--1b
select count(term) from frequency where docid='10398_txt_earn' and count=1;
--1c
select count(*) from (
select term from frequency where docid='10398_txt_earn' and count=1
UNION
select term from frequency where docid='925_txt_trade' and count=1
) x;
--1d
select count(*) from frequency where term='parliament';
--1e
select count(*) from (
select docid,sum(count) from frequency group by docid having sum(count) > 300
);
--1f
select count(*) from (
select distinct docid from frequency f1 where term='transactions'
INTERSECT
select distinct docid from frequency f2 where term='world'
);
--problem 2g
select * from (
select A.row_num,B.col_num,sum(A.value*B.value) from A,B where A.col_num = B.row_num group by A.row_num,B.col_num
) x where x.row_num = 2 and x.col_num = 3;
--problem 3h (similarity matrix)
select a.docid as q,b.docid as r,sum(a.count*b.count) 
from frequency a,frequency b
where a.term = b.term
and a.docid < b.docid
and a.docid='10080_txt_crude'
and b.docid='17035_txt_earn'
group by a.docid,b.docid;
--problem 3i (keyword search)
create view searcher as
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count;

select a.docid,sum(a.count*b.count) as similarity 
from 
(SELECT * FROM frequency where term in ('washington','taxes','treasury')) a,
searcher b
where a.term = b.term
and a.docid < b.docid
group by a.docid,b.docid
order by similarity desc
limit 10;