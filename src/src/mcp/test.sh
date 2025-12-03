#!/bin/bash

# For local
#export NEXT_GEM_DATA_CATALOG_MCP_SERVER=http://127.0.0.1:8080/mcp
export NEXT_GEM_DATA_CATALOG_MCP_SERVER=https://next-gem-catalog-mcp.fastmcp.app/mcp
uv run ./test/test_next_gem_catalog.py