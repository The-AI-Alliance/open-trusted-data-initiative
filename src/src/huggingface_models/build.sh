#!/bin/bash

poetry export -f requirements.txt >requirements.txt
docker build --network=host --progress=plain --no-cache -t huggingface_models .
docker tag huggingface_models:latest $ECR_TARGET/fargate-jobs-01/huggingface_models:latest
rm requirements.txt