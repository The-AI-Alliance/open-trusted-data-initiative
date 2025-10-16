drop table <database>.datacards_complete

/* Persistent state table for HF data cards */
CREATE TABLE <database>.datacards_complete(
    request_time timestamp,
	dataset string,
    datacard string
)
LOCATION 's3://<bucket>/<source>/datacards_complete/'
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_compression'='snappy',
  'optimize_rewrite_delete_file_threshold'='10'
)

/* View on top of the persistent table */
create or replace view <database>.v_datacards as
select * from <database>.datacards_complete

/* View to determine which datacards we should fetch on a 
   daily basis. First, ones we don't have, then padded out
   with ones we haven't downloaded lately. Combined, this
   should be about 1.2k + 5k = 6.2k per day */
create or replace view <database>.v_datacards_update as
select 
	dataset,
	request_time
from
	((select 
		d.dataset as dataset,
		d.last_modified as last_modified,
		dd.request_time as request_time
	from <database>.v_datasets d
	left join <database>.v_datacards dd
	on d.dataset = dd.dataset
	where dd.request_time  is null)
	union all
	(select 
		d2.dataset as dataset,
		d2.last_modified as last_modified,
		dd2.request_time as request_time
	from <database>.v_datasets d2
	left join <database>.v_datacards dd2
	on d2.dataset = dd2.dataset	
	order by dd2.request_time asc
	limit 5000))
order by request_time asc