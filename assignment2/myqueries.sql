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