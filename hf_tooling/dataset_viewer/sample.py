import requests
from typing import Any


# invoke API
def query(url: str) -> dict[str, Any]:
    response = requests.get(url)
    return response.json()


# Get dataset information
API_URL = "https://datasets-server.huggingface.co/info?dataset=ibm/duorc&config=SelfRC"
data = query(API_URL)
print(f"Dataset info {data}")


# Check dataset validity
API_URL = "https://datasets-server.huggingface.co/is-valid?dataset=cornell-movie-review-data/rotten_tomatoes"
data = query(API_URL)
print(f"Dataset validity info {data}")


# List configurations and splits
API_URL = "https://datasets-server.huggingface.co/splits?dataset=cornell-movie-review-data/rotten_tomatoes"
data = query(API_URL)
print(f"Dataset configuration and splits {data}")


# Preview a dataset
API_URL = "https://datasets-server.huggingface.co/first-rows?dataset=cornell-movie-review-data/rotten_tomatoes&config=default&split=train"
data = query(API_URL)
print(f"Dataset preview {data}")


# Download slices of rows
API_URL = "https://datasets-server.huggingface.co/rows?dataset=ibm/duorc&config=SelfRC&split=train&offset=150&length=10"
data = query(API_URL)
print(f"Dataset row slices {data}")


# Search text in a dataset. Only supported for datasets with Parquet exports
API_URL = "https://datasets-server.huggingface.co/search?dataset=ibm/duorc&config=SelfRC&split=train&query=dog&offset=150&length=2"
data = query(API_URL)
print(f"Dataset row slices {data}")


# Filter rows in a dataset. Only supported for datasets with Parquet exports
API_URL = 'https://datasets-server.huggingface.co/filter?dataset=ibm/duorc&config=SelfRC&split=train&where="no_answer"=true&offset=150&length=2'
data = query(API_URL)
print(f"Dataset filtered rows {data}")


# list parquet files
API_URL = "https://datasets-server.huggingface.co/parquet?dataset=ibm/duorc"
data = query(API_URL)
print(f"Dataset parquet files {data}")


# list parquet files using the Hugging Face Hub API
API_URL = "https://huggingface.co/api/datasets/ibm/duorc/parquet/"
data = query(API_URL)
print(f"Dataset parquet files {data}")


# Get the number of rows and the size in bytes
API_URL = "https://datasets-server.huggingface.co/size?dataset=ibm/duorc"
data = query(API_URL)
print(f"Dataset number rows and sizes {data}")


# Explore statistics over split data. Only supported for datasets with Parquet exports
API_URL = "https://datasets-server.huggingface.co/statistics?dataset=nyu-mll/glue&config=cola&split=train"
data = query(API_URL)
print(f"Dataset statistics over split data {data}")


# Dataset Croissant metadata
API_URL = "https://huggingface.co/api/datasets/ibm/duorc/croissant"
data = query(API_URL)
print(f"Dataset Croissant metadata {data}")
