#!/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_TARGET 
docker push $ECR_TARGET/fargate-jobs-01/get_huggingface_datasets:latest