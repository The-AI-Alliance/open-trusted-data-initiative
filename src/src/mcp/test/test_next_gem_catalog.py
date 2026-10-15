import asyncio
import logging
import os

import pytest
from fastmcp import Client

LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_server():
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.

    server_envvar = os.environ.get("NEXT_GEM_DATA_CATALOG_MCP_SERVER")
    print(f"server_envvar = {server_envvar}")
    if not server_envvar:
        LOGGER.warning(
            "Environment variable NEXT_GEM_DATA_CATALOG_MCP_SERVER not defined. Skipping this test..."
        )
    else:
        try:
            async with Client(server_envvar) as client:
                assert False, f"client: {client}"
                # List available tools
                tools = await client.list_tools()
                for tool in tools:
                    print(f">>> Tool found: {tool.name}")
                ########################################################################
                # Call get_next_gem_data_catalog_schema, perfect case
                print(">>>  Calling get_next_gem_data_catalog_schema")
                result = await client.call_tool("get_next_gem_data_catalog_schema", {})
                print(f"<<<  Result: {result.data}")
                ########################################################################
                # Call execute_sql_query, perfect case
                print(
                    ">>>  Calling execute_sql_query for select * from huggingface.v_models_latest limit 3"
                )
                result = await client.call_tool(
                    "execute_sql_query",
                    {"sql_query": "select * from huggingface.v_models_latest limit 3"},
                )
                print(f"<<<  Result: {result.content[0].text}")
                # Call execute_sql_query, bogus query
                print(">>>  Calling execute_sql_query for bogus sql")
                result = await client.call_tool(
                    "execute_sql_query", {"sql_query": "BLAH"}
                )
                print(f"<<<  Result: {result.data}")
        except Exception as e:
            print(f"Failed, reason: {e}, server envvar: {server_envvar}")
            raise


if __name__ == "__main__":
    asyncio.run(test_server())
