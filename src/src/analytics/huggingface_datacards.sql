/* SQL to create tables on top of parquet data stored in S3 */
/* and also examples of how to query them. */
/* Connect to the Athena service in the appropriate AWS region and execute */
/* Note: the data buckets should be in the same region as the Athena region, */
/* And Athena needs read and list rights to the bucket. */

/* Drop the table */
drop table huggingface.datacards

/* Create Table */
CREATE EXTERNAL TABLE IF NOT EXISTS huggingface.datacards(
    request_time string,
	dataset string,
    datacard string
)
partitioned by (`date` date)
STORED AS PARQUET
LOCATION "s3://<bucket name>/service=huggingface/datasets=datacards/";

/* Repair the table to see newly added data partitions */
MSCK REPAIR TABLE huggingface.datacards

/* Test the table by running a query */
select * from  huggingface.datacards where date = cast('2025-06-19' as date) limit 100

/* drop view*/
drop view huggingface.v_datasets

/* Create view to see just the latest COMPLETE data*/
create view huggingface.v_datacards as
select * from huggingface.datacards where date in 
	(select date from huggingface.datacards where date in 
		(select distinct date from huggingface.datacards order by date desc limit 2)
	group by date order by count(*) desc limit 1)

/* Get the counts */
select date, count(*) as total from huggingface.v_datacards group by date

/* Get the data */
select * from huggingface.v_datacards limit 100