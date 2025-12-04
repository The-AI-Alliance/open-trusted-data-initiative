CREATE EXTERNAL TABLE IF NOT EXISTS huggingface.models(
-- This table reresents the raw model data downloaded daily from Huggingface.
-- It should not be used
    request_time string,    --Time the request was made to Huggingface
    model_id string,        --The organization and model name, as presented in Huggingface
    organization string,    --Organization name
    model_name string,      --Model name
    author string,          --Author. This field is NULL for all Huggingface models
    sha string,             --Model sha. This field is NULL for all Huggingface models
    created_at string,      --Timestamp when the model was created.
    last_modified string,   --Timestamp when the model was last modified
    private boolean,        --Boolean. TRUE if the model is private.
    disabled boolean,       --Boolean. False for all mHuggingface models
    downloads int,          --Total number of times the model has been downloaded.
    downloads_all_time int, --This field is alway NULL for Huggingface models.
    gated string,           --This field is always None for Huggingface models.
    gguf string,            --This field is always NULL for Huggingface models.
    inference string,       --This field is always NULL for Huggingface models.
    likes int,              --Total number of likes for the model
    library_name string,    --Library name used to create the model
    tags  ARRAY <string>,   --List of tags associated with the model
    license string,         --License assigned to the model
    pipeline_tag string,    --How the model can be used in a data engineering pipeline
    mask_token string,      --This field is always NULL for Huggingface models.
    card_data string,       --This field is always NULL for Huggingface models.
    widget_data string,     --This field is always NULL for Huggingface models.
    model_index string,     --This field is always NULL for Huggingface models.
    config string,          --This field is always NULL for Huggingface models.
    transformers_info string,  --This field is always NULL for Huggingface models.
    trending_score int,     --This field is always NULL for Huggingface models.
    siblings string,        --This field is always NULL for Huggingface models.
    spaces string,          --This field is always NULL for Huggingface models.
   	safetensors string,     --This field is always NULL for Huggingface models.
	security_repo_status string --This field is always NULL for Huggingface models.
)
partitioned by (`date` date)

CREATE or REPLACE VIEW huggingface.v_models_latest as
-- This view represents today's clean model data downloaded from Huggingface.
Select
    cast(request_time as timestamp) as request_time,       --Time the request was made to Huggingface
    model_id,           --The organization and model name, as presented in Huggingface
    organization,       --Organization name
    model_name,         --Model name
    author,             --Author. This field is NULL for all Huggingface models
    cast(created_at as timestamp) as created_at,         --Timestamp when the model was created.
    cast(last_modified as timestamp) as last_modified,      --Timestamp when the model was last modified
    private,            --Boolean. TRUE if the model is private.
    downloads,          --Total number of times the model has been downloaded.
    likes,              --Total number of likes for the model
    library_name,       --Library name used to create the model
    tags,               --List of tags associated with the model
    license,            --License assigned to the model
    pipeline_tag        --How the model can be used in a data engineering pipeline
    date                --Date when data was downloaded from Huggingface. Partition field.
from huggingface.models
where date in (select max(date) from huggingface.models)

CREATE or REPLACE VIEW huggingface.v_models_all as
-- This view represents all clean model data downloaded from Huggingface.
Select
    cast(request_time as timestamp) as request_time,       --Time the request was made to Huggingface
    model_id,           --The organization and model name, as presented in Huggingface
    organization,       --Organization name
    model_name,         --Model name
    author,             --Author. This field is NULL for all Huggingface models
    cast(created_at as timestamp) as created_at,         --Timestamp when the model was created.
    cast(last_modified as timestamp) as last_modified,      --Timestamp when the model was last modified
    private,            --Boolean. TRUE if the model is private.
    downloads,          --Total number of times the model has been downloaded.
    likes,              --Total number of likes for the model
    library_name,       --Library name used to create the model
    tags,               --List of tags associated with the model
    license,            --License assigned to the model
    pipeline_tag        --How the model can be used in a data engineering pipeline
    date                --Date when data was downloaded from Huggingface. Partition field.
from huggingface.models