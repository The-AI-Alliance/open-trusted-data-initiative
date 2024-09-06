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

Here are the requirements to contribute a dataset to The AI Alliance Open Trusted Dataset Initiative. If you have any questions or concerns about meeting these requirements, but you are still interested in contributing, please contact us at [data@thealliance.ai](mailto:data@thealliance.ai).

## The Data Is Yours to Contribute

To ensure fully-traceable provenance and governance, you must affirm that you are the owner of the dataset or you must affirm that the dataset came from a source that offers the data for use without restriction, for example, that you have been granted permission by the owners to act on their behalf with respect to the dataset. The _data card_ has sections for specifying these details. 

> **WARNING:** Do not contribute any data that was obtained by crawling or scraping public data from the Internet. At this time, we can not accept such datasets because of concerns about verifying the provenance of all such data.

## License 

You retain all ownership, copyrights and other interests, and rights to and title to the dataset, but you grant The AI Alliance a non-exclusive, worldwide, royalty-free, perpetual, and non-cancellable license under the [Community Data License Agreement - Permissive, Version 2.0](https://cdla.dev/permissive-2-0/), which includes, but is not limited to, the ability to use, modify, alter, edit, copy, reproduce, display, make compilations of and distribute the dataset.

## Dataset Card

All useful datasets include _metadata_ about their provenance, target uses, known limitations and risks, etc. To provide a uniform, standardized way of expressing this metadata, we ask you to submit a completed _Dataset Card_ when you [contribute the dataset]({{site.baseurl}}/contributing).

Please create a copy of the [dataset card template]({{site.baseurl}}/dataset-requirements/dataset-card-template) and fill it in as instructed. After you submit this card with your dataset, we will provide feedback about clarifications needed and next steps. If you are uncertain about what a particular section requires, add questions in that section of your dataset card!

> **WARNING:** At this time, we can only accept text files with one of the following extensions: `*.txt`, `*.md`, or `*.markdown`.

## Dataset Hosting

You can either retain your current hosting location or you can have the AI Alliance host it for you.

## Some Requirements for the Data Itself

The [dataset card template]({{site.baseurl}}/dataset-requirements/dataset-card-template) has sections for all the required and optional information. Here we discuss a few points.

### Formats

We endeavor to be flexible on dataset file formats and how they are organized. For text, we recommend formats like CSV, JSON, Parquet, ORC, AVRO. Supporting PDFs, where extraction will be necessary, can be difficult, but not impossible.

## Diverse Datasets Desired for Diverse AI Models and Applications

We are particularly interested in new datasets that can be used to tune models to excel in various domains, although general-purpose datasets are also welcome. 

When you contribute a dataset, you will have the ability to optionally specify a domain specialty. To keep things relatively simple, we currently only allow one domain specialty to be specified, if any.

These are our current domains:

### Science and Industrial

* **Climate:** Supporting research in climate change, modeling vegetation and water cover, studying agriculture, etc.
* **Marine:** Supporting research on and applications targeted towards marine environments.
* **Materials:** Known chemical and mechanical properties of chemicals useful for research into potential new and existing materials. 
* **Semiconductors:** Specific area of materials research focused on improving the state of the art for semiconductor performance and manufacturing.
* **Other Industrial:** Other areas not covered above.

### Other Domains

* **Finance:** Historical market activity and behaviors. Connections to influences like climate, weather events, political events, etc. 
* **Healthcare:** Everything from synthetic patient data for modeling outcomes, to public literature on known diseases and conditions, to diagnostics results and their analysis.
* **Legal:** Jurisdiction-specific data about case law, etc.
specific applications.
* **Social Sciences:** Social dynamics, political activity and sentiments, etc.
* **Timeseries:** Data for training, tuning, and testing time series models, including specific applications.

In addition, we will ask you clarify the _modality_ of the data. It may contain one or more of the following:

* **Text Only**
* **Image:** (still images)
* **Audio:** 
* **Video:** (including optional audio)


### Categorization

We will ask you to specify the dataset's _modality_, i.e., is the dataset text-only, images, audio, video, or combinations thereof. We also ask you to indicate the target domain (e.g., time series), if any.

### Data Quality and &ldquo;Cleanliness&rdquo;

We support several levels of quality and cleanliness, as follows. This list corresponds to stages in our _ingestion_ process:

* **Raw:** The dataset as submitted, which could already be in good shape. _Our most important criteria at this stage is **unambigious provenance**._ Raw datasets will go through filtering and analysis to remove potential objectionable content. However, the presence of some content in the raw data could have legal implications, such as some forms of PII and company confidential information, which may force us to reject the contribution. (Should this happen, we will discuss mitigation options with you.)
* **Filtered:** A _raw_ dataset has gone through our processing pipeline to remove duplicates, filter for objectional content, etc.
* **Structured:** A _filtered_ dataset has been reformated to be most suitable for model training (LLMs, time series, etc.), RAG patterns, and similar purposes. For example, JSON-formatted data is often desirable. 

See [How We Process Datasets]({{site.baseurl}}/our-processing) for more details on these levels and how we process datasets.

Next, prepare the [dataset card]({{site.baseurl}}/dataset-requirements/dataset-card-template) and [contribute your dataset!]({{site.baseurl}}/contributing).

