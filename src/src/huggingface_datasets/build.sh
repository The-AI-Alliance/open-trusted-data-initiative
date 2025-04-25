#!/bin/bash

poetry export -f requirements.txt >requirements.txt
docker build --progress=plain --no-cache -t get_huggingface_datasets .
docker tag get_huggingface_datasets:latest $ECR_TARGET/fargate-jobs-01/get_huggingface_datasets:latest
rm requirements.txt