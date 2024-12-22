# Dataset Viewer API

An alternative to the [`data_access` APIs](../data_access/README.md) is to use the REST API for the [dataset viewer](https://huggingface.co/docs/dataset-viewer/quick_start). This API can be used to:

* Check whether a dataset on the Hub is functional.
* Return the subsets and splits of a dataset.
* Preview the first 100 rows of a dataset.
* Download slices of rows of a dataset.
* Search a word in a dataset.
* Filter rows based on a query string.
* Access the dataset as parquet files.
* Get the dataset size (in number of rows or bytes).
* Get statistics about the dataset.

The [sample.py](sample.py) code demonstrates the API. Consult the [documentation](https://huggingface.co/docs/dataset-viewer/quick_start) for the available API endpoints.
