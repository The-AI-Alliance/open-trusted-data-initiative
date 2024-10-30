---
layout: default
title: How We Process Datasets
nav_order: 30
has_children: false
show_contribute_dataset_button: true
---

# How We Process Datasets

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Provenance and Governance

Given the importance of provenance and governance for the datasets in this initiative, we will analyze all proposed datasets to ensure they meet our [dataset requirements]({{site.baseurl/dataset-requirements/dataset-requirements}}). We will publish the technical details of these processes soon. The [Data and Trust Alliance](https://dataandtrustalliance.org/) standard for [provenance](https://dataandtrustalliance.org/work/data-provenance-standards) will inform our work.

## Data Quality and &ldquo;Cleanliness&rdquo;

In [Dataset Requirements]({{site.baseurl}}/dataset-requirements/dataset-requirements), we described several levels of quality and cleanliness that we use to categorize datasets. Think of this as a rough outline of our _ingestion_ process:

* **Raw:** The dataset as submitted, which could already be in good shape. _Our most important criteria at this stage is **unambigious provenance**._ Nevertheless, datasets that contain some objectionable content with legal implications, such as some forms of PII and company confidential information, may have to be rejected outright, or we will decide to only include the _filtered_ version of the dataset in our catalog.
* **Filtered:** A _raw_ dataset has gone through our processing pipeline to remove duplicates, filter for objectional content, etc.
* **Structured:** A _filtered_ dataset has been reformated to be most suitable for model training (LLMs, time series, etc.), RAG patterns, and similar purposes. For example, JSON-formatted data is often desirable. 

## How We Process Datasets

To go from **Raw** to **Filtered**, we use a process with the following checks (which will evolve over time):

* **An initial quality check:**
  * Acceptable format
  * Not corrupted (e.g., a valid PDF)
  * No evident inconsistencies in the data vs. the datacard metadata, e.g., in licensing.
* **Filtering:**
  * Duplicate removal
  * Remove low-quality data (e.g., HTML tags)
  * PII removal
  * Copyright data removal (where feasible)
  * Toxic content removal
  * Bias
  * Decontamination against known evaluation and benchmark datasets
  * License verification (where feasible, detect data known to be covered by a different, incompatible license)
  * Other consistency and quality improvements

The transformations to create **Structured** datasets are TBD, but may include one or more of the following:

* Tokenization
* Conversion to JSON or YAML
* &ldquo;Chunkification&rdquo; (e.g., for use in RAG data stores)

All steps include auditing provenance and lineage with full visibility available to users of the datasets.
