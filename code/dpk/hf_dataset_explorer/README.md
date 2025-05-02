HF Dataset Explorer Transform
The HF dataset explorer transform reads are going through the datasets, rather then a list of
files, reading Readme file and extracting Dataset card. At the moment it only extracts the license
information from the card, but can be extended to extract additional information.

The following runtimes are available:

* [python](src/hf_dataset_explorer/python) - provides the base python-based transformation
implementation.
* [ray](src/hf_dataset_explorer/ray) - enables the running of the base python transformation
in a Ray runtime

## Summary

This transform is going through all of the HF datasets extracting dataset card. It further extracts
the value of the `licanse`. As a result it publishes a metadata file, containing counts and
percentage of every license (name) across all datasets.