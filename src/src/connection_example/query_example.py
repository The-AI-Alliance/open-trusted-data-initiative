import logging
import os

import awswrangler as wr
import boto3

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)


def execute_sql_query(sql_query: str):
    """This function will execute a valid SQL statement against the OTD Catalog
        and return the results as a csv file.

    Args:
        sql_query: A valid SQL statement for the OTD schema.

    Returns:
        Query results in csv fromat.
    """
    try:
        logger.info(f"Executing sql: {sql_query}")
        boto3.setup_default_session(region_name=os.environ["AWS_REGION"])

        logger.info("Connecting to AWS Athena")
        results_df = wr.athena.read_sql_query(
            sql=sql_query,
            database=os.environ["OTD_CATALOG_DATABASE_NAME"],
            athena_cache_settings={
                "max_cache_seconds": 90,
            },
        )
        logger.info("Query Executed")
        return results_df.to_csv(index=False)
    except Exception as e:  # noqa: BLE001
        msg = f"Unable to execute query: {e}"
        logger.info(msg)
        return msg


def main():
    print("What about you?")


if __name__ == "__main__":
    print(
        execute_sql_query(
            "select dataset, tags from datasets_complete where contains(tags,'language:fr') limit 100"
        )
    )
