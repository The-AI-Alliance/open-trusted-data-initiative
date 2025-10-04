# Purpose of code is to get a list of all data sets in HuggingFace Hub.
# Uses the HF Datasets API to get them, persist them to S3, then use that
# then perform an upsert into the main state table.

from huggingface_hub import HfApi
import pandas as pd
import awswrangler as wr
from datetime import datetime, timezone
import boto3
import os
import time


# Upsert daily results into main state table.
# Will redundantly upsert the last three days data in the event
# the job fails at some point. Epected case is 1.5k datasets will change from
# day to day, meaning this will execute on about 4.5k datasets daily.
def merge_query(date: str):
    return_val = f""" 
merge into {os.environ["ATHENA_DATABASE_NAME"]}.datasets_complete as target
using (select * from {os.environ["ATHENA_DATABASE_NAME"]}.datasets where date = cast('{date}' as date) and date(last_modified)>(cast('{date}' as date) - interval '3' day)) as source
on target.dataset=source.dataset
when matched then
    update set
        request_time = CURRENT_TIMESTAMP,
        organization = lower(source.author),
        dataset_name = lower(replace(source.dataset,source.author||'/' , '')),
        created_at = source.created_at,   
        last_modified = source.last_modified,
        private = source.private,
        disabled = source.disabled,
        gated = source.gated,
        downloads = source.downloads,
        downloads_all_time= source.downloads_all_time,
        tags = source.tags, 
        license = source.license,
        trending_score = source.trending_score
when not matched then
    insert (request_time, dataset, organization, dataset_name, created_at, last_modified, private, disabled, gated, downloads, downloads_all_time, tags, license, trending_score)
    values (current_timestamp, source.dataset, lower(source.author), lower(replace(source.dataset,source.author||'/' , '')), source.created_at, source.last_modified, source.private, source.disabled, source.gated, source.downloads, source.downloads_all_time, source.tags, source.license, source.trending_score)
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
    sql = f"MSCK REPAIR TABLE {os.environ["ATHENA_DATABASE_NAME"]}.datasets"
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
output_datasets = []
# TODO: Move this to the param store or pass in via aws cdk
key = "/service=huggingface/datasets=datasets/"
target_s3_bucket = f"s3://{os.environ["ANALYTICS_BUCKET"]}{key}"

today = datetime.today().strftime("%Y-%m-%d")
print(f"Starting run: {today}")
print(f"ANALYTICS_BUCKET: {os.environ["ANALYTICS_BUCKET"]}")
print(f"ANALYTICS_OUTPUT_BUCKET: {os.environ["ANALYTICS_OUTPUT_BUCKET"]}")
print(f"AWS_REGION: {os.environ["AWS_REGION"]}")
print(f"ATHENA_DATABASE_NAME: {os.environ["ATHENA_DATABASE_NAME"]}")
print(f"NUMBER_OF_DATASETS_TO_REQUEST: {os.environ["NUMBER_OF_DATASETS_TO_REQUEST"]}")

# Documentation:
# https://huggingface.co/docs/huggingface_hub/v0.27.1/en/package_reference/hf_api#huggingface_hub.DatasetInfo
hf_input_datasets = []

try:
    # Making the below HF API call will return HTTP 429 if not limited...
    hf_input_datasets = list(
        api.list_datasets(
            sort="lastModified",
            direction=-1,
            limit=int(os.environ["NUMBER_OF_DATASETS_TO_REQUEST"]),
        )
    )

    print(f"\tSuccessfully got datasets. Total number: {len(hf_input_datasets)}")
except Exception as e:
    print(f"Error getting datasets from HuggingFace: {e}")

for dataset in hf_input_datasets:
    this_data_set = {}

    # Partition column
    this_data_set["date"] = today
    # Athena does not support timestamps with timezones
    # https://docs.aws.amazon.com/athena/latest/ug/data-types.html
    this_data_set["request_time"] = (
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
    )

    this_data_set["dataset"] = dataset.id
    this_data_set["author"] = dataset.author
    this_data_set["created_at"] = dataset.created_at
    this_data_set["last_modified"] = dataset.last_modified
    this_data_set["private"] = dataset.private
    this_data_set["disabled"] = dataset.disabled
    this_data_set["gated"] = str(
        dataset.gated
    )  # Could be the boolean 'False' or a string...
    this_data_set["downloads"] = dataset.downloads
    this_data_set["downloads_all_time"] = dataset.downloads_all_time
    this_data_set["tags"] = dataset.tags
    for tag in dataset.tags:
        if "license" in tag:
            this_data_set["license"] = tag.replace("license:", "")
    this_data_set["trending score"] = dataset.trending_score
    # https://huggingface.co/docs/huggingface_hub/v0.27.1/en/package_reference/cards#huggingface_hub.DatasetCardData
    if dataset.card_data:
        this_data_set["dataset card license"] = dataset.card_data.license
        this_data_set["dataset card source"] = dataset.card_data.source_datasets
        this_data_set["dataset card size"] = dataset.card_data.size_categories
    output_datasets.append(this_data_set)

print(
    f"\tSuccessfully processed {len(hf_input_datasets)} datasets. Writing to {target_s3_bucket}."
)
if len(hf_input_datasets) > 0:
    output_df = pd.DataFrame.from_dict(output_datasets)

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

    # Merge into huggingface.datasets_full
    print("Start merge")
    todays_merge_query = merge_query(date=datetime.today().strftime("%Y-%m-%d"))
    print(f"Merge query: {todays_merge_query}")
    success = do_merge(todays_merge_query)
    print(f"End merge. Status: {success}")

else:
    print("No datasets to process. Exiting.")
