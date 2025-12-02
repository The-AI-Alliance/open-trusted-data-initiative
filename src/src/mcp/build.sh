#!/bin/bash
uv pip freeze > requirements.txt
docker build --network=host --progress=plain --no-cache -t next_gem_catalog_mcp_server .
docker tag next_gem_catalog_mcp_server:latest $ECR_TARGET/mcp-servers/next_gem_catalog_mcp_server:latest
rm requirements.txt