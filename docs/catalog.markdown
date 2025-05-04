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

> **TODO:** We plan to provide an integrated search and browsing feature, to make it easier to select the datasets for your particular needs. See [below](#searching-for-datasets) for suggestions on how to find open datasets you need in the meantime. Also, the current catalog is a provisional list of datasets; we are not yet validating them against our draft [requirements]({{site.baseurl}}/dataset-requirements).

## Datasets by Categories ("Tags")

### Languages

{% for language in site.language %}
<a name="{{language.tag}}"></a>
<div class="table-wrapper">
  <table>
    <tbody>
      <tr>
        <td>
          <a href="{{site.baseurl}}/catalog/#{{language.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph width-100 text-center">{{language.name}}</a>
          <p>{{language.content | htmlify }}</p>
        </td>
      </tr>
    </tbody>
  </table>
</div>
{% endfor %}

### Domains

{% for domain in site.domain %}
<a name="{{domain.tag}}"></a>
<div class="table-wrapper">
  <table>
    <tbody>
      <tr>
        <td>
          <a href="{{site.baseurl}}/catalog/#{{domain.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph width-100 text-center">{{domain.name}}</a>
          <p>{{domain.content | htmlify }}</p>
        </td>
      </tr>
    </tbody>
  </table>
</div>
{% endfor %}

### Modalities

{% for modality in site.modality %}
<a name="{{modality.tag}}"></a>
<div class="table-wrapper">
  <table>
    <tbody>
      <tr>
        <td>
          <a href="{{site.baseurl}}/catalog/#{{modality.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph width-100 text-center">{{modality.name}}</a>
          <p>{{modality.content | htmlify }}</p>
        </td>
      </tr>
    </tbody>
  </table>
</div>
{% endfor %}

## Dataset Sources

The following organizations, shown in alphabetical order, maintain open data sets that are part of our catalog.

> **NOTE:** See also the AI Alliance's [Hugging Face organization](https://huggingface.co/aialliance){:target="aia-hf"} and the [Open Trusted Data Initiative catalog](https://huggingface.co/collections/aialliance/open-trusted-data-catalog-66d21b3cb66342762fb6108e){:target="aia-hf-otdi"} there that includes the datasets listed here.

### BrightQuery

[BrightQuery](https://brightquery.ai/){:target="bq"} ("BQ") provides proprietary financial, legal, and employment information on private and public companies derived from regulatory filings and disclosures. BQ proprietary data is used in capital markets for investment decisions, banking and insurance for KYC & credit checks, and enterprises for master data management, sales, and marketing purposes. In addition, BQ provides public information consisting of clean and standardized statistical data from all the major government agencies and NGOs around the world, and is doing so in partnership with the source agencies. BQ public datasets will be published in OTDI spanning all topics: economics, demographics, healthcare, crime, climate, education, sustainability, etc. Much of the data will be tabular (i.e., structured) time series data, as well as unstructured text.

_More specific information is coming soon._

### Common Crawl Foundation

[Common Crawl Foundation](https://commoncrawl.org/){:target="ccf"} is working on tagged and filtered crawl subsets for English and other languages.

_More specific information is coming soon._

### EPFL 

The [EPFL LLM team](https://huggingface.co/epfl-llm){:target="epfl-llm"} has curated a dataset to train their [Meditron](https://github.com/epfLLM/meditron){:target="meditron"} models. An open-access subset of the medical guidelines data is published on [Hugging Face](https://huggingface.co/datasets/epfl-llm/guidelines){:target="guidelines"}

See the Meditron GitHub repo [README](https://github.com/epfLLM/meditron?tab=readme-ov-file#medical-training-data){:target="meditron-readme"} for more details about the whole dataset used to train Meditron.

### Meta

[Data for Good at Meta](https://dataforgood.facebook.com/dfg/){:target="dfg"} empowers partners with privacy-preserving data that strengthens communities and advances social issues. Data for Good is helping organizations respond to crises around the world and supporting research that advances economic opportunity.

There are 220 datasets available. See [Meta's page](https://data.humdata.org/organization/meta){:target="humdata"} at the [Humanitarian Data Exchange](https://data.humdata.org/){:target="humdata"} for the full list of datasets.

### PleIAs

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

### ServiceNow

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

### SemiKong

The training dataset for the [SemiKong](https://www.semikong.ai/){:target="semikong"} collaboration that trained an open model for the semiconductor industry.

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **SemiKong** | An open model training dataset for semiconductor technology | [Hugging Face](https://huggingface.co/datasets/pentagoniac/SemiKong_Training_Datset){:target="semikong-dataset"} | 2024-09-01 |

## Make Your Contributions!

To expand this catalog, we [welcome contributions]({{site.baseurl}}/contributing).

<!-- To expand this catalog, we not only [welcome contributions]({{site.baseurl}}/contributing), but we plan to seek out qualified datasets leveraging other sources of information about them, such as the [Data Provenance Initiative](https://www.dataprovenance.org/){:target="dp"}, [Hugging Face](https://huggingface.co/datasets){:target="hf-datasets"}, and others (TBD). -->

## Other Ways to Search For Datasets

Until our catalog search is fully operational, there are several ways you can search for datasets that match your criteria.

### Hugging Face Hub Search

You can do [full-text search](https://huggingface.co/search/full-text?type=dataset){:target="hf-search"} for datasets, models, and organization spaces in the [Hugging Face Hub](https://huggingface.co/){:target="hf-hub"}. Uncheck _models_ and _spaces_ on the left-hand side to limit your search to datasets. 

For example, searching for _apache croissant_ finds datasets licensed with the Apache 2.0 license that support Croissant metadata. However, using _cdla_ (for Common Data License Agreement) instead of _apache_ also finds a dataset named _CDLA_.

### Google Dataset Search

[Google Dataset Search](https://datasetsearch.research.google.com/){:target="google-ds-search"} is a powerful search engine that finds datasets matching specific criteria across a range of repositories, including Hugging Face.

For example, [this query](https://datasetsearch.research.google.com/search?src=0&query=*&docid=L2cvMTFsZjZjY25jbg%3D%3D&filters=WyJbXCJoYXNfY3JvaXNzYW50X2Zvcm1hdFwiXSIsIltcImZpZWxkX29mX3N0dWR5XCIsW1wibmF0dXJhbF9zY2llbmNlc1wiXV0iLCJbXCJpc19hY2Nlc3NpYmxlX2Zvcl9mcmVlXCJdIl0%3D&property=aXNfYWNjZXNzaWJsZV9mb3JfZnJlZQ%3D%3D){:target="google-ds-search-example"} finds datasets with [Croissant metadata]() that have permissive licenses allowing free and commercial use, and are focused on the natural sciences. 
