---
layout: default
title: How We Process Datasets
nav_order: 40
has_children: false
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

<!--
  Possible tools:
  1. Dolma Toolkit
  2. DPK
  3. Various "guardian" tools
-->

## Provenance and Governance

Given the importance of provenance and governance for the datasets in this initiative, we plan to analyze proposed datasets to ensure they meet our [dataset specification]({{site.baseurl}}/dataset-requirements). _Derived_ datasets that do various forms of filtering are also planned, as discussed below.

We will publish the technical details of these processes as they are developed. We will open source all source code and deployment information for these pipelines under the AI Alliance standard code license: [_Apache 2.0_](https://spdx.org/licenses/Apache-2.0){:target="apache"}. (See the Alliance [`community/CONTRIBUTING` page](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md#licenses){:target="licenses"} for more details about our license conventions.)

## Data Quality and &ldquo;Cleanliness&rdquo;

In [Dataset Specification]({{site.baseurl}}/dataset-requirements), we described several levels of quality and cleanliness that guide aspects of how we categorize datasets in our catalog. Think of the following as a rough outline of our _ingestion_ and processing steps:

* **Raw:** The dataset as submitted. _Our most important criteria at this stage is **unambigious provenance**._ Raw datasets may contain some objectionable content, but appropriate labels and usage guidance will be provided. For example, a dataset with hate speech may be suitable for use by researchers studying hate speech and working on detectors for it, but model developers may decide to avoid the dataset. However, in some cases, legal or other considerations may prevent us from accepting some content without additional filtering.
* **Filtered:** A dataset created by passing a _raw_ dataset through a processing pipeline to perform modifications such as removal of duplicate data, filtering for objectional content, etc.
* **Structured:** A dataset created from a _filtered_ dataset where the new structure is more suitable for model training (LLMs, time series, etc.), RAG usage, tuning, and other purposes. For example, JSON-formatted data is often desirable. 

## How We Process Datasets - Proposed

To go from **Raw** to **Filtered**, we currently plan to use processes with the following checks and filtering steps. These lists will mature over time:

### Raw Data Ingestion

An initial quality analysis is performed, including the following checks:

* Meets the [Dataset Specification]({{site.baseurl}}/dataset-requirements) - e.g., license, provenance, etc.
* No evident corruption - e.g., PDFs, JSON, etc. have valid formats.
* No detectable inconsistencies between the data vs. the datacard metadata.

### Creating a Filtered Dataset 

There could be several filtered dataset that are derived from a single raw dataset, each of which would use one or more of the following transformations:

* Exact and &ldquo;fuzzy&rdquo; duplication
* Removal of low-quality content (e.g., HTML tags)
* PII removal
* Removal of copyrighted data (where detectable)
* Removal of data covered by non-open access licenses (where detectable)
* Toxic content removal (e.g., bias, hate speech, etc.)
* Decontamination from known, public datasets for benchmarks and other evaluations
* Other consistency and quality improvements

### Creating a Structured Dataset

The transformations to create one more structured datasets from a filtered dataset may include one or more of the following:

* Tokenization
* Conversion to JSON, YAML, or other format
* Conversion of PDFs and other &ldquo;rich&rdquo; formats to text and images
* Embedding - encoding with an encoding model and chunkifying for use in RAG and similar patterns

## For All Processing

All ingestion and transformation steps will include full auditing to support data governance specification, so that full provenance and lineage back to original sources is tracked, with full visibility available to users of the datasets. _Each_ dataset will have its governance metadata in its own dataset card that is publically available with the dataset. For example, it can be used to create _Bills of Material_ by interested parties (see [here]({{site.baseurl}}/references/#ai-bom)).
