drop table <database>.datasets_detail_complete

/* Equals signs not allowed in the LOCATION for some reason... */
CREATE TABLE <database>.datasets_detail_complete (
	dataset				string,
	request_time 		timestamp,
	response			int,
	response_reason		string,
	croissant			string
) 
LOCATION 's3://<bucket>/<source>/datases_detail_complete/'
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_compression'='snappy',
  'optimize_rewrite_delete_file_threshold'='10'
)

create or replace view <database>.v_datasets_detail as
select * from  <database>.datasets_detail_complete

create or replace view <database>.v_croissant_update as
select 
	dataset,
	request_time
from
	((select 
		d.dataset as dataset,
		d.last_modified as last_modified,
		dd.request_time as request_time
	from <database>.v_datasets d
	left join <database>.v_datasets_detail dd
	on d.dataset = dd.dataset
	where dd.request_time  is null)
	union all
	(select 
		d2.dataset as dataset,
		d2.last_modified as last_modified,
		dd2.request_time as request_time
	from <database>.v_datasets d2
	left join <database>.v_datasets_detail dd2
	on d2.dataset = dd2.dataset	
	order by dd2.request_time asc
	limit 40000))
order by request_time asc