drop table huggingface.datasets_detail_complete

/* Equals signs not allowed in the LOCATION for some reason... */
CREATE TABLE huggingface.datasets_detail_complete (
	dataset				string,
	request_time 		timestamp,
	response			int,
	response_reason		string,
	croissant			string
) 
LOCATION 's3://anl-analytics-us-east-2/huggingface/datases_detail_complete/'
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_compression'='snappy',
  'optimize_rewrite_delete_file_threshold'='10'
)

create or replace view huggingface.v_datasets_detail as
select * from  huggingface.datasets_detail_complete

create or replace view huggingface.v_croissant_update as
select 
	dataset,
	request_time
from
	((select 
		d.dataset as dataset,
		d.last_modified as last_modified,
		dd.request_time as request_time
	from huggingface.v_datasets d
	left join huggingface.v_datasets_detail dd
	on d.dataset = dd.dataset
	where dd.request_time  is null)
	union all
	(select 
		d2.dataset as dataset,
		d2.last_modified as last_modified,
		dd2.request_time as request_time
	from huggingface.v_datasets d2
	left join huggingface.v_datasets_detail dd2
	on d2.dataset = dd2.dataset	
	order by dd2.request_time asc
	limit 40000))
order by request_time asc