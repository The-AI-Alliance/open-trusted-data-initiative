
/* Table runs on top of the .csv output produced by the OTDI scoring job */
/* This is intended to be searched using AWS Athena and presented using
   the OTDI catalog */

DROP TABLE IF EXISTS aialliance.otdi;

CREATE EXTERNAL TABLE IF NOT EXISTS aialliance.otdi(
	dataset	string,
	datacard_date string,	
	dataset_size double,	
	yaml_section_count int,	
	markdown_section_count int,
	score float,
	score_date string,	
	license string,	
	license_name string,	
	license_link string,	
	extra_gated_fields string,	
	task_categories string,	
	source_datasets	string,
	pretty_name	string,
	language_details string,	
	row_license boolean, 
	metadata_fields	string,
	features string,
	notes string
)
partitioned by (`date` date)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   'separatorChar' = ',',
   'quoteChar' = '"',
   'escapeChar' = '\\'
   )
STORED AS TEXTFILE
LOCATION "s3://<s3-bucket>/service=huggingface/datasets=otdi/"
TBLPROPERTIES (
  "skip.header.line.count"="1"
  )

/* drop view */
drop view aialliance.v_otdi

/* Create view with latest data */
create view aialliance.v_otdi as
    select * from aialliance.otdi where date in (select max(date) from aialliance.otdi)  