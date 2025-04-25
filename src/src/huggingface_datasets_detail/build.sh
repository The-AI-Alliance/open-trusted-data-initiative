#!/bin/bash
poetry export -f requirements.txt >requirements.txt
docker build --progress=plain --no-cache -t get_huggingface_datasets_detail .
docker tag get_huggingface_datasets_detail:$ECR_TARGET/fargate-jobs-01/get_huggingface_datasets_detail:latest
rm requirements.txt