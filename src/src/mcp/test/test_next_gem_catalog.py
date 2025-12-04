import asyncio
import os

from fastmcp import Client


async def test_server():
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.

    try:
        async with Client(os.environ.get("NEXT_GEM_DATA_CATALOG_MCP_SERVER")) as client:

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
            result = await client.call_tool("execute_sql_query", {"sql_query": "BLAH"})
            print(f"<<<  Result: {result.data}")
    except Exception as e:
        print(f"Failed, reason: {e}")


if __name__ == "__main__":
    asyncio.run(test_server())
