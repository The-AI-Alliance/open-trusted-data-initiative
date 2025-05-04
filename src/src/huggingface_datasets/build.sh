#!/bin/bash

poetry export -f requirements.txt >requirements.txt
docker build --network=host --progress=plain --no-cache -t huggingface_datasets .
docker tag huggingface_datasets:latest $ECR_TARGET/fargate-jobs-01/huggingface_datasets:latest
rm requirements.txt