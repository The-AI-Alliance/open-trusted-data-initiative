# Purpose of code is to get a list of all data sets in HuggingFace Hub.
# Uses the HF Datasets API to get them, persist them to S3, then use that
# then perform an upsert into the main state table.

from huggingface_hub import HfApi
import pandas as pd
import awswrangler as wr
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError
import os
import time
import json


def get_secret_value(secret_name, region_name="us-east-2"):
    """
    Retrieve a secret value from AWS Secrets Manager
    
    Args:
        secret_name: The name or ARN of the secret
        region_name: AWS region where the secret is stored
    
    Returns:
        The secret value (string or dict)
    """
    
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        
        # Secrets can be stored as either string or binary
        if 'SecretString' in response:
            secret = response['SecretString']
            # If it's a JSON string, parse it
            try:
                return json.loads(secret)
            except json.JSONDecodeError:
                return secret
        else:
            # Binary secret
            return response['SecretBinary']
            
    except ClientError as e:
        # Handle specific errors
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Secret {secret_name} not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print(f"Invalid request for secret {secret_name}")
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print(f"Invalid parameter for secret {secret_name}")
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print(f"Cannot decrypt secret {secret_name}")
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print(f"Internal service error retrieving {secret_name}")
        raise e

    


# Upsert daily results into main state table.
# Will redundantly upsert the last three days data in the event
# the job fails at some point. Epected case is 1.5k datasets will change from
# day to day, meaning this will execute on about 4.5k datasets daily.
def merge_query(date: str):
    return_val = f""" 
merge into {os.environ["ATHENA_DATABASE_NAME"]}.models_complete as target
using {os.environ["ATHENA_DATABASE_NAME"]}.v_models as source
on target.model_id=source.model_id
when matched then
    update set
		request_time = CURRENT_TIMESTAMP,
		model_id = source.model_id,
		organization = split_part(source.model_id,'/', 1),
		model_name =  split_part(source.model_id,'/', 2),
		author = source.author,
		sha = source.sha,
		created_at = source.created_at,
		last_modified = source.last_modified, 
		private = source.private,
		disabled = source.disabled,
		downloads = source.downloads,
		downloads_all_time =source.downloads_all_time,
		gated = source.gated,
		gguf =source.gguf,
		inference =source.inference,
		likes =source.likes,
		library_name =source.library_name,
		tags = source.tags,
		license = source.license,
		pipeline_tag = source.pipeline_tag,
		mask_token  = source.mask_token,
		card_data = source.card_data,
		widget_data = source.widget_data,
		model_index  = source.model_index,
		config  = source.config,
		transformers_info = source.transformers_info,
		trending_score = source.trending_score,
		siblings = source.siblings,
		spaces =source.spaces,
		safetensors = source.safetensors,
		security_repo_status = source.security_repo_status
when not matched then
    insert (request_time, model_id, organization, model_name, author, sha, created_at, last_modified, private, disabled, downloads, downloads_all_time, gated, gguf, inference, likes, library_name, tags, license, pipeline_tag, mask_token, card_data, widget_data, model_index, config, transformers_info, trending_score, siblings, spaces, safetensors, security_repo_status)
    values (CURRENT_TIMESTAMP, source.model_id, split_part(source.model_id,'/', 1), split_part(source.model_id,'/', 2), source.author, source.sha, source.created_at, source.last_modified, source.private, source.disabled, source.downloads, source.downloads_all_time, source.gated, source.gguf, source.inference, source.likes, source.library_name, source.tags, source.license, source.pipeline_tag, source.mask_token, source.card_data, source.widget_data, source.model_index, source.config, source.transformers_info, source.trending_score, source.siblings, source.spaces, source.safetensors, source.security_repo_status) 
    """
    return return_val


# Evaluate what the state of a query is. This is used twice:
# Once for MSCK REPAIR TABLE and the second for the upsert.
def has_query_succeeded(client, execution_id):
    state = "RUNNING"
    max_execution = 10

    while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
        max_execution -= 1
        response = client.get_query_execution(QueryExecutionId=execution_id)
        if (
            "QueryExecution" in response
            and "Status" in response["QueryExecution"]
            and "State" in response["QueryExecution"]["Status"]
        ):
            state = response["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                return "Success"

        time.sleep(30)
    if max_execution == 0:
        return "Failed - Query state never tranisitioned to SUCCEEDED and timed out"
    else:
        return response["QueryExecution"]["Status"]["AthenaError"]


# AWS Athena implements schema-on-read as Hive, need to execute this
# to refresh the data after write in order to query it later.
# MSCK REPAIR TABLE executed as an Athena query.
# TODO: Bucket and region will be passed in from aws cdk when we get there
def repair_table():
    boto3.setup_default_session(region_name=os.environ["AWS_REGION"])
    client = boto3.client("athena")

    config = {
        "OutputLocation": f"s3://{os.environ["ANALYTICS_OUTPUT_BUCKET"]}/huggingface/output/",
    }

    # Query Execution Parameters
    sql = f"MSCK REPAIR TABLE {os.environ["ATHENA_DATABASE_NAME"]}.models"
    context = {"Database": os.environ["ATHENA_DATABASE_NAME"]}

    response = client.start_query_execution(
        QueryString=sql, QueryExecutionContext=context, ResultConfiguration=config
    )
    success = has_query_succeeded(client, response["QueryExecutionId"])
    return success


# Execute the upsert
def do_merge(merge_query: str):
    # TODO: Session should be shared with repair_table()
    boto3.setup_default_session(region_name=os.environ["AWS_REGION"])
    client = boto3.client("athena")

    config = {
        "OutputLocation": f"s3://{os.environ["ANALYTICS_OUTPUT_BUCKET"]}/huggingface/output/",
    }

    # Query Execution Parameters
    sql = merge_query
    context = {"Database": os.environ["ATHENA_DATABASE_NAME"]}

    response = client.start_query_execution(
        QueryString=sql, QueryExecutionContext=context, ResultConfiguration=config
    )
    success = has_query_succeeded(client, response["QueryExecutionId"])
    return success


api = HfApi()
output_models = []
# TODO: Move this to the param store or pass in via aws cdk
key = "/service=huggingface/datasets=models/"
target_s3_bucket = f"s3://{os.environ["ANALYTICS_BUCKET"]}{key}"
token = get_secret_value(os.environ["SECRET_NAME"])["token"]
today = datetime.today().strftime("%Y-%m-%d")

print(f"Starting run: {today}")
print(f"ANALYTICS_BUCKET: {os.environ["ANALYTICS_BUCKET"]}")
print(f"ANALYTICS_OUTPUT_BUCKET: {os.environ["ANALYTICS_OUTPUT_BUCKET"]}")
print(f"AWS_REGION: {os.environ["AWS_REGION"]}")
print(f"ATHENA_DATABASE_NAME: {os.environ["ATHENA_DATABASE_NAME"]}")
print(f"NUMBER_OF_MODELS_TO_REQUEST: {os.environ["NUMBER_OF_MODELS_TO_REQUEST"]}")
print(f"HF TOKEN: {token[-5:]}")
# Documentation:
# https://huggingface.co/docs/huggingface_hub/v0.27.1/en/package_reference/hf_api#huggingface_hub.DatasetInfo
hf_input_models = []

try:
    # Making the below HF API call will return HTTP 429 if not limited...
    hf_input_models = list(
        # https://huggingface.co/docs/huggingface_hub/package_reference/hf_api#huggingface_hub.HfApi.list_models.emissions_thresholds
        api.list_models(
            sort="lastModified",
            direction=-1,
            token=token,
            limit=int(os.environ["NUMBER_OF_MODELS_TO_REQUEST"]),
        )
    )

    print(f"\tSuccessfully got models. Total number: {len(hf_input_models)}")
    #print(hf_input_models[1])
except Exception as e:
    print(f"Error getting models from HuggingFace: {e}")

for model in hf_input_models:
    this_model = {}

    # Partition column
    this_model["date"] = today
    # Athena does not support timestamps with timezones
    # https://docs.aws.amazon.com/athena/latest/ug/data-types.html
    this_model["request_time"] = (
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
    )

    this_model["model_id"] = model.id
    this_model["organization"] = model.id.split("/")[0]
    this_model["model_name"] = model.id.split("/")[1]
    this_model["author"] = model.author
    this_model["sha"] = model.sha
    this_model["created_at"] = model.created_at.strftime("%Y-%m-%d %H:%M:%S")
    this_model["last_modified"] = ""
    if model.last_modified:
        this_model["last_modified"] = model.last_modified.strftime("%Y-%m-%d %H:%M:%S")
    this_model["private"] = model.private
    this_model["disabled"] = model.disabled
    this_model["downloads"] = model.downloads
    this_model["downloads_all_time"] = model.downloads_all_time
    this_model["gated"] = str(
        model.gated
    )  # Could be the boolean 'False' or a string...

    this_model["gguf"] = model.gguf
    this_model["inference"] = model.inference
    this_model["likes"] = model.likes
    this_model["library_name"] = model.library_name
    this_model["tags"] = model.tags
    for tag in model.tags:
        if "license" in tag:
            this_model["license"] = tag.replace("license:", "")

    this_model["pipeline_tag"] = model.pipeline_tag
    this_model["mask_token"] = model.mask_token
    this_model["card_data"] = model.card_data
    this_model["widget_data"] = model.widget_data
    this_model["model_index"] = model.model_index
    this_model["config"] = model.config
    this_model["transformers_info"] = model.transformers_info
    this_model["trending_score"] = None
    if model.trending_score:
        this_model["trending_score"] = round(model.trending_score)
    this_model["siblings"] = model.siblings
    this_model["spaces"] = model.spaces
    this_model["safetensors"] = model.safetensors
    this_model["security_repo_status"] = model.security_repo_status

    output_models.append(this_model)

print(
    f"\tSuccessfully processed {len(hf_input_models)} models. Writing to {target_s3_bucket}."
)
#print(json.dumps(output_models, indent=3))

if len(hf_input_models) > 0:
    output_df = pd.DataFrame.from_dict(output_models)

    # Write to S3
    output_files = wr.s3.to_parquet(
        df=output_df,
        path=target_s3_bucket,
        dataset=True,
        partition_cols=["date"],
        mode="append",
    )

    print(
        f"\tSuccessfully wrote dataframe of dimensions {output_df.shape} to {output_files}."
    )
    
    print("Start repairing table")
    success = repair_table()
    print(f"End repairing table. Status: {success}")
       
    # Merge into huggingface.models_full
    print("Start merge")
    todays_merge_query = merge_query(date=datetime.today().strftime("%Y-%m-%d"))
    print(f"Merge query: {todays_merge_query}")
    success = do_merge(todays_merge_query)
    print(f"End merge. Status: {success}")
    
else:
    print("No models to process. Exiting.")