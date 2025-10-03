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

/*
 Creates a persistent Iceberg table that will contain the current state
 of all datasets. This table will be upserted into once a day with 
 datasets that have been modified.
*/

drop table <database>.datasets_complete

/* Equals signs not allowed in the LOCATION for some reason... */
CREATE TABLE <database>.datasets_complete (
    request_time timestamp,
	dataset string,
    organization string,
    dataset_name string,
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
LOCATION 's3://<bucket>/iceberg/'
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_compression'='snappy',
  'optimize_rewrite_delete_file_threshold'='10'
)