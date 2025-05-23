/* SQL to create tables on top of parquet data stored in S3 */
/* and also examples of how to query them. */
/* Connect to the Athena service in the appropriate AWS region and execute */
/* Note: the data buckets should be in the same region as the Athena region, */
/* And Athena needs read and list rights to the bucket. */

/* Create database...*/
create database huggingface;

/* Drop data sets table. Note this is schema on read so no */ 
/* data is deleted, just the schema */
drop table huggingface.datasets


/* Create data sets table */
CREATE EXTERNAL TABLE IF NOT EXISTS huggingface.datasets(
    request_time string,
	dataset string,
    author string,
    created_at timestamp,   
    last_modified timestamp,
    private boolean,
    disabled boolean,
    gated string,
    downloads int,
    downloads_all_time int,
    tags ARRAY <string>, 
    license string,
    trending_score double
)
partitioned by (`date` date)
STORED AS PARQUET
/* Replace <bucket> tag below with appropriate bucket name */
LOCATION "s3://<bucket>/service=huggingface/datasets=datasets/";

/* Add new partitions */
MSCK REPAIR TABLE huggingface.datasets

/* Execute a query based on a date */
select * from huggingface.datasets where date = CAST('2025-02-13' AS DATE) limit 100

/* Drop detailed data sets table. Note this is schema on read so no */
/* data is deleted, just the schema */
drop table huggingface.datasets_detail

/* Create detailed data sets table */
CREATE EXTERNAL TABLE IF NOT EXISTS huggingface.datasets_detail(
	dataset				string,
	request_time 		string,
	response			int,
	response_reason		string,
	croissant			string
)
partitioned by (`date` date)
STORED AS PARQUET
/* Replace <bucket> tag below with appropriate bucket name */
LOCATION "s3://<bucket>/service=huggingface/datasets=datasets_detail/";

/* Add new partitions */
MSCK REPAIR TABLE huggingface.datasets_detail

/* Execute a query based on a date */
select * from huggingface.datasets_detail where date = CAST('2025-02-13' AS DATE) limit 100


/* Since the datasets_detail job takes so long to run, these views will return */
/* the last, most complete data set */
/* For both views, use the row count in datasets_details to determine which date to use*/

/* drop view*/
drop view huggingface.v_datasets as

/* Create view*/
create view huggingface.v_datasets as
select * from huggingface.datasets where date in 
	(select date from huggingface.datasets_detail where date in 
		(select distinct date from huggingface.datasets_detail order by date desc limit 2)
	group by date order by count(*) desc limit 1)

/* Get the counts */
select date, count(*) as total from huggingface.v_datasets group by date
/* Get the data */
select * from huggingface.v_datasets limit 100

/* drop view*/
drop view huggingface.v_datasets_detail

/* Create view*/
create view huggingface.v_datasets_detail as
select * from huggingface.datasets_detail where date in 
	(select date from huggingface.datasets_detail where date in 
		(select distinct date from huggingface.datasets_detail order by date desc limit 2)
	group by date order by count(*) desc limit 1)

/* Get the counts */
select date, count(*) as total from huggingface.v_datasets_detail group by date
/* Get the data */
select * from huggingface.v_datasets_detail limit 100