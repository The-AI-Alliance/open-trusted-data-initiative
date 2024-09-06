---
layout: default
title: Dataset Requirements
nav_order: 20
has_children: true
show_contribute_dataset_button: true
---

# Dataset Requirements

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

Here are the requirements to contribute a dataset to the Open Trusted Dataset Initiative.

## The Data Is Yours to Contribute

To ensure fully-traceable provenance and governance, you must be the owner of the data you want to donate or you must affirm that this data came from a source that offers the data for use without restriction. The _data card_ has sections for specifying details. 

## License

All OTDI datasets must support permissive usage, including for commercial purposes. Therefore, we require that _all contributed datasets_ support the [CDLA Permissive 2.0](https://cdla.dev/permissive-2-0/) license ([SPDX link](https://spdx.org/licenses/CDLA-Permissive-2.0.html)). If for some reason this license requirement is difficult to satisfy, but you are still interested in contributing, please reach out to us at [data@thealliance.ai](mailto:data@thealliance.ai).

## Dataset Card

All useful datasets include _metadata_ about their provenance, target uses, known limitations and risks, etc. To provide a uniform, standardized way of expressing this metadata, we ask you to submit a completed _Dataset Card_ when you [contribute the dataset]({{site.baseurl}}/contributing).

Please create a copy of the [dataset card template text]({{site.baseurl}}/dataset-requirements/dataset-card-template) and fill it in as instructed. After you submit this card with your dataset, we will provide feedback about clarifications needed and next steps. If you are uncertain about what a particular section requires, add questions in that section of your dataset card!

> **WARNING:** At this time, we can only accept text files with one of the following extensions: `*.txt`, `*.md`, or `*.markdown`.

## Requirements for the Data Itself

### Formats

We endeavor to be flexible on dataset file formats and how they are organized. For text, we recommend formats like CSV, JSON, Parquet, ORC, AVRO. Supporting PDFs, where extraction will necessary, can be difficult.

### Categorization

We will ask you to specify the dataset's _modality_, i.e., is the dataset text-only or multimodal. 

### Data Quality and &ldquo;Cleanliness&rdquo;

We support several levels of quality and cleanliness, as follows. Think of this as the _ingestion_ process we use:

* **Raw:** The dataset as submitted, which could already be in good shape. _Our most important criteria at this stage is unambigious provenance._ Nevertheless, datasets that contain some objectionable content with legal implications, such as some forms of PII and company confidential information, may have to be rejected outright.
* **Filtered:** A _raw_ dataset has gone through our processing pipeline to remove duplicates, filter for objectional content, etc.
* **Structured:** A _filtered_ dataset has been reformated to be most suitable for model training (LLMs, time series, etc.), RAG patterns, and similar purposes. For example, JSON-formatted data is often desirable. 

The filtering process will involve the following (at the time of this writing):

* **An initial quality check:**
  * Acceptable format
  * Not corrupted (e.g., a valid PDF)
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

All steps will audit provenance and lineage with full visibility available to users of the datasets.

The structured transformations may include one or more of the following:

* Tokenization
* Conversion to JSON or YAML
* &ldquo;Chunkification&rdquo; (e.g., for use in RAG data stores)

