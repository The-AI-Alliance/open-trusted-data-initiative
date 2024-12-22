from huggingface_hub import HfApi


# instance APIs. Additionally can get repo endpoint and access token
api = HfApi()

sets = api.list_datasets(limit=10)
for dataset in sets:
    print(dataset)