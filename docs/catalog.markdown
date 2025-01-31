---
layout: default
title: Dataset Catalog
nav_order: 20
has_children: false
---

# The Dataset Catalog

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

See also the AI Alliance's [Hugging Face organization](https://huggingface.co/aialliance){:target="aia-hf"} and the [Open Trusted Data Initiative catalog](https://huggingface.co/collections/aialliance/open-trusted-data-catalog-66d21b3cb66342762fb6108e){:target="aia-hf-otdi"} there that includes the datasets listed here.

> **TODO:** We plan to provide an integrated search and browsing feature, to make it easier to select the datasets for your particular needs. 

Here is the current list of datasets, organized by owner.

> **BETA:** This is a provisional list of datasets. We are not yet validating datasets against our draft [requirements]({{site.baseurl}}/dataset-requirements).

## BrightQuery

[BrightQuery](https://brightquery.ai/){:target="bq"} ("BQ") provides proprietary financial, legal, and employment information on private and public companies derived from regulatory filings and disclosures. BQ proprietary data is used in capital markets for investment decisions, banking and insurance for KYC & credit checks, and enterprises for master data management, sales, and marketing purposes. In addition, BQ provides public information consisting of clean and standardized statistical data from all the major government agencies and NGOs around the world, and is doing so in partnership with the source agencies. BQ public datasets will be published in OTDI spanning all topics: economics, demographics, healthcare, crime, climate, education, sustainability, etc. Much of the data will be tabular (i.e., structured) time series data, as well as unstructured text.

_More specific information is coming soon._

## Common Crawl Foundation

[Common Crawl Foundation](https://commoncrawl.org/){:target="ccf"} is working on tagged and filtered crawl subsets for English and other languages.

_More specific information is coming soon._

## Meta

[Data for Good at Meta](https://dataforgood.facebook.com/dfg/){:target="dfg"} empowers partners with privacy-preserving data that strengthens communities and advances social issues. Data for Good is helping organizations respond to crises around the world and supporting research that advances economic opportunity.

There are 220 datasets available. See [Meta's page](https://data.humdata.org/organization/meta){:target="humdata"} at the [Human Data Exchange](https://data.humdata.org/){:target="humdata"} for the full list of datasets.

## PleIAs

Domain-specific, clean datasets. 

* PleIAs [website](https://pleias.fr){:target="pleias"}
* PleIAs [Hugging Face organization](https://huggingface.co/PleIAs){:target="pleias-hf"}.
* PleIAs [Collections on Hugging Face](https://huggingface.co/collections/PleIAs){:target="pleias-hf-col"}

| Name             | Description     |  URL     | Date Added |
| :--------------- | :-------------- | :------- | :--------- |
| **Common Corpus** | Largest multilingual pretraining data | [Hugging Face](https://huggingface.co/collections/PleIAs/common-corpus-6734e0f67ac3f35e44075f93){:target="common-corpus"} | 2024-11-04 |
| **Toxic Commons** | Tools for de-toxifying public domain data, especially multilingual and historical text data and data with OCR errors | [Hugging Face](https://huggingface.co/collections/PleIAs/toxic-commons-672243e8ce64b6759e79b6dc){:target="toxic-commons"} | 2024-11-04 |
| **Finance Commons** | A large collection of multimodal financial documents in open data | [Hugging Face](https://huggingface.co/collections/PleIAs/finance-commons-66925e1095c7fa6e6828e26c){:target="finance-commons"} | 2024-11-04 |
| **Bad Data Toolbox** | PleIAs collection of models for the data processing of challenging document and data sources | [Hugging Face](https://huggingface.co/collections/PleIAs/bad-data-toolbox-66981c2d0df662459252844e){:target="bad-data-toolbox"} | 2024-11-04 |
| **Open Culture** | A multilingual dataset of public domain books and newspapers | [Hugging Face](https://huggingface.co/collections/PleIAs/openculture-65d46e3ea3980fdcd66a5613){:target="open-culture"} | 2024-11-04 |

## ServiceNow

Multimodal, code, and other datasets. 

* ServiceNow [website](https://www.servicenow.com){:target="servicenow"}
* ServiceNow [Hugging Face organization](https://huggingface.co/ServiceNow){:target="servicenow-hf"}
* BigCode [Hugging Face organization](https://huggingface.co/bigcode){:target="big-code-hf"}

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **BigDocs-Bench** | A dataset for a comprehensive benchmark suite designed to evaluate downstream tasks that transform visual inputs into structured outputs, such as GUI2UserIntent (fine-grained reasoning) and Image2Flow (structured output). We are actively working on releasing additional components of BigDocs-Bench and will update this repository as they become available. | [Hugging Face](https://huggingface.co/datasets/ServiceNow/BigDocs-Bench){:target="bigdocs-bench"} | 2024-12-11 |
| **RepLiCA**   | RepLiQA is an evaluation dataset that contains Context-Question-Answer triplets, where contexts are non-factual but natural-looking documents about made up entities such as people or places that do not exist in reality... | [Hugging Face](https://huggingface.co/datasets/ServiceNow/repliqa){:target="replica"} | 2024-12-11 |
| **The Stack** | Exact deduplicated version of [The Stack](https://www.bigcode-project.org/docs/about/the-stack/){:target="the-stack"} dataset used for the [BigCode project](https://www.bigcode-project.org){:target="big-code"}. | [Hugging Face](https://huggingface.co/datasets/bigcode/the-stack){:target="the-stack-hf"} | 2024-12-11 |
| **The Stack Dedup** | Near deduplicated version of The Stack (recommended for training). | [Hugging Face](https://huggingface.co/datasets/bigcode/the-stack-dedup){:target="the-stack-dedup"} | 2024-12-11 |
| **StarCoder Data** | Pretraining dataset of [StarCoder](https://huggingface.co/blog/starcoder){:target="starcoder"}. | [Hugging Face](https://huggingface.co/datasets/bigcode/starcoderdata){:target="starcoderdata"} | 2024-12-11 |

## SemiKong

The training dataset for the [SemiKong](https://www.semikong.ai/){:target="semikong"} collaboration that trained an open model for the semiconductor industry.

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **SemiKong** | An open model training dataset for semiconductor technology | [Hugging Face](https://huggingface.co/datasets/pentagoniac/SemiKong_Training_Datset){:target="semikong-dataset"} | 2024-09-01 |

## Your Contributions?

To expand this catalog, we [welcome contributions]({{site.baseurl}}/contributing).

<!-- To expand this catalog, we not only [welcome contributions]({{site.baseurl}}/contributing), but we plan to seek out qualified datasets leveraging other sources of information about them, such as the [Data Provenance Initiative](https://www.dataprovenance.org/){:target="dp"}, [Hugging Face](https://huggingface.co/datasets){:target="hf-datasets"}, and others (TBD). -->
