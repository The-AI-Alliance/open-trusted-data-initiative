import asyncio
import logging
import os
import time

from fastmcp import FastMCP
import boto3
import awswrangler as wr
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("MCP server for the Next Gem Data Catalog")


@mcp.tool()
def get_next_gem_data_catalog_schema() -> str:
    """This tool will return the schema (DDL) for the Next Gem Data Catalog.

    Args:
        None

    Returns:
        String format of the DDL for the Next Gem Data Catalog.
    """
    # Below is not supported on FastMCP Cloud
    try:
        s3 = boto3.client("s3", region_name=os.environ["AWS_REGION"])
        response = s3.get_object(
            Bucket=os.environ["ANALYTICS_BUCKET"],
            Key="schemas/next_gem_data_catalog_schema.ddl",
        )
        return response["Body"].read().decode("utf-8")
    except Exception as e:
        return f"Error getting schema for the Next Gem Data Catalog. Error: {e}"


@mcp.tool()
def execute_sql_query(sql_query: str):
    """This tools will execute a valid SQL statement against the Next Gem Data Catalog
        and return the results as a csv file.

    Args:
        sql_query: A valid SQL statement for the Next Gem Data Catalog schema.

    Returns:
        Query results in csv fromat.
    """
    try:
        logger.info(f"Executing sql: {sql_query}")
        boto3.setup_default_session(region_name=os.environ["AWS_REGION"])

        logger.info(f"Connecting to Athena")
        results_df = wr.athena.read_sql_query(
            sql=sql_query, database=os.environ["NEXT_GEM_DATA_CATALOG_DATABASE_NAME"]
        )
        logger.info(f"Query Executed")
        return results_df.to_csv(index=False)
    except Exception as e:
        msg = f"Unable to execute query: {e}"
        logger.info(msg)
        return msg


if __name__ == "__main__":
    logger.info(f" MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            # transport="http",
            transport="streamable-http",
            # host="127.0.0.1",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )
