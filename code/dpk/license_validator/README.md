# License Validator Transform
The License validator transforms reads license information for each individual document in the data
set and creates a metadata file containing a percentage of each license across all documents
of a simple 1:1 transform.  The following runtimes are available:

* [python](src/license_validator/python) - provides the base python-based transformation
  implementation.
* [ray](src/license_validator/ray) - enables the running of the base python transformation
  in a Ray runtime

## Summary

This transform is going through all of the pyarrow files in the data set and for every row tries to get
the value of the `licanse` (configurable) column. As a result it publishes a metadata file, containing
percentage of every license (name) across all documents 