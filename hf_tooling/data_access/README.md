# Hub Python Library

The huggingface_hub library is a library for interacting with the Hugging Face Hub, which is a 
collection of git-based repositories (models, datasets or Spaces). There are two main ways to 
access the Hub using huggingface_hub. `Git-based` approach, implemented by the Repository class - a wrapper around 
the git command with additional functions specifically designed to interact with the Hub. `HTTP-based` approach, 
involves making HTTP requests using the HfApi client (compare to [PyGithub](https://github.com/PyGithub/PyGithub)).

The main advantage of using a Repository is that it allows you to maintain a local copy of the entire repository on 
your machine. This can also be a disadvantage as it requires you to constantly update and maintain this local copy.

The HfApi class provides an alternative to local git repositories, which can be cumbersome to maintain, especially 
when dealing with large models or datasets. The HfApi class offers the same functionality as git-based approaches, 
such as downloading and pushing files and creating branches and tags, but without the need for a local folder that 
needs to be kept in sync. In addition to the functionalities already provided by git, the HfApi class offers additional 
features, such as the ability to manage repos, download files using caching for efficient reuse, search the Hub for 
repos and metadata, access community features such as discussions, PRs, and comments, and configure Spaces hardware 
and secrets.

In our evaluation we looked only at HfApi and only at its usage for working with datasets

## Installation

The library can be installed using the following command:

```commandline
pip install huggingface_hub
```

## Create and manage datasets

Library provides a wealth of APIs 
(using [HfApi Client](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#hfapi-client))
to create, delete and manage repository. This includes support for:

* creating [repository](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.create_repo) (dataset)
* creating [pull request](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.create_pull_request)
* merging [pull request](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.merge_pull_request)
* creating [branch](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.create_branch)
* create [discussion](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.create_discussion)
* create [tag](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.create_tag)
* create [webhook](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.create_webhook)

And many others. Refer to HfApi documentation for more details

## Search datasets

Library provides very simple and straightforward APIs for exploring assets in Hugging face hub,
see this simple [code example](ds_explorer.py). See additional 
[parameters](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api#huggingface_hub.HfApi.list_datasets)
for more options on filtering, ordering and paging of the search parameters.

## Working with the dataset cards

Simple example of reading of dataset card is [here](dataset_card.py)
The same class `DatasetCard` can also beused for creating of a new card

# Accessing dataset data

Library also provides Apis for [download](https://huggingface.co/docs/huggingface_hub/main/en/guides/download) and
[upload](https://huggingface.co/docs/huggingface_hub/main/en/guides/upload) files. This apis provide support
for access (downloading and uploading) of individual files and directories, but their capabilities are
sort of limited.

A more flexible approach is provided by `Filesystem API`. A simple example showing its capabilities is
[here](file_system.py). For all methods on this class refer to 
[documentation](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_file_system#huggingface_hub.HfFileSystem)

# Parquet support

Dataset files can be in every format, for example, JSON, CSV, etc. When uploaded to the dataset, these 
files are automatically converted to parquet (using parquet-converter bot) and are stored (in the Parquet format) in 
`the refs/convert/parquet branch`. As explained [here](https://huggingface.co/datasets/haibaraconan/video/discussions/1),
when the dataset is already in Parquet format, the data are not converted and the files in refs/convert/parquet are 
links to the original files. This rule has an exception to ensure the dataset viewer API to stay fast: if the row 
group size of the original Parquet files is too big, new Parquet files are generated.