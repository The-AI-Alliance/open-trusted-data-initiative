#!/bin/bash
poetry export -f requirements.txt --without-hashes >requirements.txt
docker build --network=host --progress=plain --no-cache -t huggingface_datasets_detail .
docker tag huggingface_datasets_detail:latest $ECR_TARGET/fargate-jobs-01/huggingface_datasets_detail:latest
rm requirements.txt