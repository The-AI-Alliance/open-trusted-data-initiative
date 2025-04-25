# Purpose of code is to retreive the croissant metadata for all the  data sets
# in HuggingFace Hub.
# Uses the HF Datasets API to get them, then stores them as parquet files
# in S3 so they can be queried using serverless SQL (AWS Athena) later.
# This makes one API call for each dataset, so it is an intensive job.
# Trick is to keep the requests under the undocumented HF API limiter.
# Implemented job is scheduled to run for an hour 4x a day.

from datetime import datetime, timezone
import awswrangler as wr
import asyncio
from aiohttp import (
    ClientSession,
    TCPConnector,
    ClientConnectionError,
    ClientResponseError,
)

import pandas as pd
import boto3
from time import time
import random
import math
from http import HTTPStatus
import sys
import os

counter = 0


# AWS Athena implements schema-on-read as Hive, need to execute this
# to refresh the data after write in order to query it later.
# MSCK REPAIR TABLE executed as an Athena query.
# TODO: Bucket and region will be passed in from aws cdk when we get there
def repair_table():
    boto3.setup_default_session(region_name="us-east-1")
    client = boto3.client("athena")

    config = {
        "OutputLocation": f"s3://{os.environ("ANALYTICS_BUCKET")}/huggingface/output/",
    }

    # Query Execution Parameters
    sql = "MSCK REPAIR TABLE hf_datasets_detail"
    context = {"Database": "default"}

    client.start_query_execution(
        QueryString=sql, QueryExecutionContext=context, ResultConfiguration=config
    )


# This is intended to keep the parallelly executed API calls under the undocumented
# API rate limit.
class RateLimiter(object):
    def __init__(self, delay, jitter=0.1):
        self._lock = asyncio.Lock()
        self._delay = delay
        self._jitter = jitter
        self._next_time = time()

    async def wait(self):
        async with self._lock:
            now = time()
            if now < self._next_time:
                await asyncio.sleep(self._next_time - now)
            self._next_time = (
                time() + self._delay + random.uniform(-self._jitter, self._jitter)
            )


async def process_row(id, batch_id, session, limiter):
    try:
        url = f"https://huggingface.co/api/datasets/{id}/croissant"
        await limiter.wait()
        response = await session.request(method="GET", url=url)
        global counter
        counter = counter + 1

        this_metadata = {}
        if response.status not in [
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]:
            this_metadata["date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            this_metadata["dataset"] = id
            # Athena does not support timestamps with timezones
            # https://docs.aws.amazon.com/athena/latest/ug/data-types.html
            this_metadata["request_time"] = (
                datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
            )
            this_metadata["response"] = response.status
            this_metadata["response_reason"] = str(response.reason)
            this_metadata["croissant"] = ""
            this_metadata["croissant"] = await response.text()

    except ClientConnectionError as e:
        print(f"Connection error: {e} for {url}")
        pass
    except ClientResponseError as e:
        print(f"HTTP error: {e.status} - {e.message} for {url}")
        pass
    except asyncio.TimeoutError as e:
        print(f"Request timed out for {url}")
        pass
    except ValueError as e:
        print(f"Error getting croissant data: {e} for {url}")
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e} for {url}")
        pass

    if len(this_metadata) == 0:
        return None
    else:
        return this_metadata


# Parallel execution. Acceptable rate limits found via experiment.
async def process_batch(batch_id, batch):
    print(f"Processing batch: {batch_id}")
    connector = TCPConnector(limit=1, limit_per_host=1)
    async with ClientSession(connector=connector) as session:
        limiter = RateLimiter(
            0.2, 0.05
        )  # Throttle to not overload the HF API...Need to avoid the 429 response codes.
        results = await asyncio.gather(
            *[
                process_row(row["dataset"], batch_id, session, limiter)
                for index, row in batch.iterrows()
            ],
            return_exceptions=True,
        )
    filtered_results = [result for result in results if result is not None]
    output_df = pd.DataFrame(filtered_results)
    print(f"Closing Session {batch_id}")
    await session.close()
    return output_df


# Let's get croissant data for HF data where we do not already have it today.
async def main():
    number_of_partitions = 4
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    limit = "limit 100000"
    query = f"select distinct dataset from hf_datasets where dataset not in (select dataset from hf_datasets_detail where date = CAST('{today}' AS DATE)) and date = CAST('{today}' AS DATE) {limit}"
    boto3.setup_default_session(
        region_name="us-east-1"
    )  # TODO: This limit and region will be passed in from aws cdk when we get there

    try:
        input_df = wr.athena.read_sql_query(sql=query, database="default")
        print(f"Input dimensions: {input_df.shape}")

        batch_size = math.ceil(input_df.shape[0] / number_of_partitions)
        print(f"Batch size: {batch_size}")
        batches = [
            input_df[i : i + batch_size]
            for i in range(0, input_df.shape[0], batch_size)
        ]
    except ValueError as e:
        print(f"Exception generating input datafrane: {e}")
        sys.exit(1)

    tasks = [process_batch(i, batch) for i, batch in enumerate(batches)]

    processed_batches = await asyncio.gather(*tasks, return_exceptions=False)
    print(f"Concating dataframe")
    final_df = pd.concat(processed_batches)
    print(f"Final dataframe shape: {final_df.shape}")
    print(f"Final dataframe types: {final_df.dtypes}")

    paths = wr.s3.to_parquet(
        df=final_df,
        path=f"s3://{os.environ("ANALYTICS_BUCKET")}/huggingface/datasets_detail/",
        dataset=True,
        partition_cols=["date"],
        mode="append",  # Could be append, overwrite or overwrite_partitions
    )

    print(f"\tWrote file(s): {paths}")

    print("Start repairing table")
    repair_table()
    print("End repairing table")


if __name__ == "__main__":
    asyncio.run(main())
