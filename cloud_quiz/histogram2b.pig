register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar
--fs -mkdir /user/hadoop --store output
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
subjects = group ntriples by (subject) PARALLEL 50;
count_by_subject = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;
count2 = group count_by_subject by (count) PARALLEL 50;
histogram = foreach count2 generate flatten($0) as x, COUNT($1) as y PARALLEL 50; 
--store histogram into '/user/hadoop/histogram-results' using PigStorage();
store histogram into 's3n://courseradatascience/histogram2b-results';