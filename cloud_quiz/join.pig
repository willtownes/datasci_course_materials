register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
--raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
-- later you will load to other files, example:
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

--filter tuples by subject matching value of interest
interesting = filter ntriples by subject matches '.*rdfabout\\.com.*';
--interesting = filter ntriples by subject matches '.*business.*'; --testfile mode

--make copy of interesting data
interesting2 = foreach interesting generate subject as subject2, predicate as predicate2, object as object2;

--create join
join1 = join interesting by object, interesting2 by subject2 PARALLEL 50;
--join1 = join interesting by subject, interesting2 by subject2 PARALLEL 50; --testfile mode

--filter out duplicates
join2 = DISTINCT join1;

--store local mode
--store join2 into '/tmp/finaljoinoutput' using PigStorage();

--store the results in the folder /user/hadoop/join-results
--store join2 into '/user/hadoop/join-results' using PigStorage();

--store the results in Amazon S3 bucket
store join2 into 's3n://courseradatascience/join-results';