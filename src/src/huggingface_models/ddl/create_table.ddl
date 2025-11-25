drop table <database>.models
CREATE EXTERNAL TABLE IF NOT EXISTS <database>.models(
    request_time string,
    model_id string,
    organization string,
    model_name string,
    author string,
    sha string,
    created_at string,
    last_modified string,
    private boolean,
    disabled boolean,
    downloads int,
    downloads_all_time int,
    gated string,
    gguf string,
    inference string,
    likes int,
    library_name string,
    tags  ARRAY <string>, 
    license string,
    pipeline_tag string,
    mask_token string, 
    card_data string,
    widget_data string,
    model_index string,
    config string,
    transformers_info string,
    trending_score int,
    siblings string,
    spaces string,
   	safetensors string,
	security_repo_status string
)
partitioned by (`date` date)
STORED AS PARQUET
LOCATION "s3://<bucket_name>/service=<service>/datasets=models/";

MSCK REPAIR TABLE <database>.models

create or replace view <database>.v_models as
    select * from  <database>.models where date=current_date

drop table <database>.models_complete

CREATE TABLE <database>.models_complete(
    request_time timestamp,
    model_id string,
    organization string,
    model_name string,
    author string,
    sha string,
    created_at string,
    last_modified string,
    private boolean,
    disabled boolean,
    downloads int,
    downloads_all_time int,
    gated string,
    gguf string,
    inference string,
    likes int,
    library_name string,
    tags  ARRAY <string>, 
    license string,
    pipeline_tag string,
    mask_token string, 
    card_data string,
    widget_data string,
    model_index string,
    config string,
    transformers_info string,
    trending_score int,
    siblings string,
    spaces string,
   	safetensors string,
	security_repo_status string
)
LOCATION 's3://<bucket_name>/<database>/models_complete/'
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_compression'='snappy',
  'optimize_rewrite_delete_file_threshold'='10'
)