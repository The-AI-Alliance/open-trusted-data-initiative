#!/bin/bash
poetry export -f requirements.txt --without-hashes >requirements.txt
docker build --network=host --progress=plain --no-cache -t huggingface_datacards .
docker tag huggingface_datacards:latest $ECR_TARGET/fargate-jobs-01/huggingface_datacards:latest
rm requirements.txt