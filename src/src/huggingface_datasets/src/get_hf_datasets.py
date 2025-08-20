# Purpose of code is to get a list of all data sets in HuggingFace Hub.
# Uses the HF Datasets API to get them, then stores them as parquet files
# in S3 so they can be queried using serverless SQL (AWS Athena) later.

from huggingface_hub import HfApi
import pandas as pd
import awswrangler as wr
from datetime import datetime, timezone
import boto3
import os


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

    client.start_query_execution(
        QueryString=sql, QueryExecutionContext=context, ResultConfiguration=config
    )


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

# Documentation:
# https://huggingface.co/docs/huggingface_hub/v0.27.1/en/package_reference/hf_api#huggingface_hub.DatasetInfo
hf_input_datasets = []
try:
    hf_input_datasets = list(api.list_datasets())
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
output_df = pd.DataFrame.from_dict(output_datasets)
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
repair_table()
print("End repairing table")
