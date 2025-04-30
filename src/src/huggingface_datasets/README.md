# HuggingFace Data Sets

## Purpose
The purpose of this project is to capture the entire list of data sets that reside on HuggingFace Hub. This is accomplished using the HuggingFace Hub `HFApi` Python SDK. 

## Implementation
Code is developed as a Docker job intended to execute once a day, and store the results as a parquet file in an S3 data lake. The data in the data lake is meant to be consumed using SQL powered by AWS Athena.

Project consits of the daily job source code, which includes the write-to-S3 data lake. It also consists of a connection to the AWS Athena service. AWS Athena is based on Apache Hive, and the daily job writes a new file object and inferred partition daily in the form of `date=YYYY-MM-DD` as part of the key to the object. Athena will have to execute `MSCK REPAIR TABLE` to make the new daily partition queryable.

## Execution
Job is intended to be run as an AWS Fargate job, triggered using AWS EventBridge and monitored using AWS CloudWatch,

The `Dockerfile`, `build.sh`, `push.sh` and `run.sh` scrips are included to facilitate development and testing, both local and remote.

## To Dos
1. No AWS deployment code is present, this needs to be implemented using AWS CDK.
2. The 'write parquet file' functionality should be isolated from the 'repair database' functionality. The latter should be moved to its own job triggered by the first.
3. Project needs further work to ensure it can be deployed and execute by anyone using their own AWS account.
4. A better strategy would be to figure out how to share the resulting data with the community, rather than have them reproduce the compute and storage process.