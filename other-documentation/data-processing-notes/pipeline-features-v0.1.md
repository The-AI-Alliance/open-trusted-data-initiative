# Proposed V0.1 Pipeline Features

January 2025

## Assumptions

* Only process datasets hosted in Hugging Face.
* Implement support for only some of the "required" fields in the [requirements](https://the-ai-alliance.github.io/open-trusted-data-initiative/dataset-requirements/) for this iteration.

## Analyze Dataset Cards

For each dataset:

1. Check that the dataset has a dataset card, a root-folder `README.md`.
1. Check that the metadata in the dataset card lists a valid license:
	a. `license` - one of the names listed [here](https://huggingface.co/docs/hub/repositories-licenses)
1. Check that `license` is one of the following allowed licenses:
	* CDLA 2.0
	* Apache 2.0
	* CC-BY-4.0
	* MIT

1. Check that the following metadata is non-empty:
	* `dataset_card_authors`
	* `dataset_issue_date` - a valid date string, preferably `YYYY-mm-dd:THH:MM:SS`.
	* `language_details` - e.g., one or more of `en-US`, `fr-FR`, etc.
	* `source_datasets`

## Verify the License Requirements

1. Look for a root-folder license file
	a. If present, does the content match the declared `license` and `license_link` in the dataset card?
1. Scan the dataset scheme for a `license` column. 
	a. If found, does the content match the declared `license` and `license_link` in the dataset card?
	a. If found, do all entries fall within the set of allowed licenses above?
1. (Stretch goal) Scan the dataset for other license files, using "reasonable" heuristics.
	b. If present, are they consistent with the declared license?