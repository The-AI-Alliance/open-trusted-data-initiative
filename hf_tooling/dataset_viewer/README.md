# Dataset viewer API


An alternative to the [dataaccess APIs](../data_access) is usage of the the dataset viewer’s REST API. 
These APIs can be used to:

* Check whether a dataset on the Hub is functional.
* Return the subsets and splits of a dataset.
* Preview the first 100 rows of a dataset.
* Download slices of rows of a dataset.
* Search a word in a dataset.
* Filter rows based on a query string.
* Access the dataset as parquet files.
* Get the dataset size (in number of rows or bytes).
* Get statistics about the dataset.

A simple code demonstrating these APIs is [here](sample.py)
Consult [documentation](https://huggingface.co/docs/dataset-viewer/quick_start) for the availble
API endpoints
