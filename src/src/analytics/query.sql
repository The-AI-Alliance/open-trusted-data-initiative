# SQL to create tables on top of parquet data stored in S3 
# and also examples of how to query them.

drop table hf_datasets

CREATE EXTERNAL TABLE IF NOT EXISTS hf_datasets(
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
LOCATION "s3://<bucket>/huggingface/datasets/";
MSCK REPAIR TABLE hf_datasets

select * from hf_datasets where date = CAST('2025-02-13' AS DATE) limit 100


drop table hf_datasets_detail

CREATE EXTERNAL TABLE IF NOT EXISTS hf_datasets_detail(
	dataset				string,
	request_time 		string,
	response			int,
	response_reason		string,
	croissant			string
)
partitioned by (`date` date)
STORED AS PARQUET
LOCATION "s3://<bucket>/huggingface/datasets_detail/";
MSCK REPAIR TABLE hf_datasets_detail


select * from hf_datasets_detail limit 100 

select distinct dataset from hf_datasets where dataset not in (select dataset from hf_datasets_detail where date = CAST('2025-02-13' AS DATE))
and date = CAST('2025-02-13' AS DATE)