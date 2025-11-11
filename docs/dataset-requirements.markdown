---
layout: default
title: Dataset Specification
nav_order: 30
has_children: false
---

# Dataset Specification

{: .note}
> **Note:** The specification documented here is the &ldquo;V0.1.6&rdquo; version of the criteria we believe are required for datasets cataloged by OTDI. We need and welcome your feedback! Either [contact us]({{site.baseurl}}/about/#contact-us) or consider using [pull requests](https://github.com/The-AI-Alliance/open-trusted-data-initiative/pulls){:target="prs"} with your suggestions. See the AI Alliance community page on [contributing](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md){:target="contrib"} for more details.
>
> Also [contact us]({{site.baseurl}}/about/#contact-us) if you are interested in contributing a dataset, but you have any questions or concerns about meeting the following specification.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## About This Specification

The specification attempts to be _minimally sufficient_, to impose just enough constraints to meet our goals for cataloged datasets.

### Sources and Inspirations

The details of the specification and how we are implementing it build on the prior and parallel work of several organizations:

* The metadata fields and concepts defined for [Hugging Face Dataset Cards](https://huggingface.co/docs/hub/datasets-cards){:target="hf-card"}, with a few extensions and clarifications for our provenance and governance purposes.
* MLCommons [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} for the metadata storage format. Croissant is an emerging de facto standard for metadata. It is used by Hugging Face and other dataset repositories for cataloging metadata and providing search capabilities.
* Some defined metadata fields are inspired by the [Data Provenance Standard](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"} from the [Data and Trust Alliance](https://dataandtrustalliance.org/){:target="dta"}.
* [The Stack](https://huggingface.co/datasets/bigcode/the-stack){:target="thestack"} dataset for the BigCode model project. See the [dataset card](https://huggingface.co/datasets/bigcode/the-stack#dataset-card-for-the-stack){:target="hf-dataset-card"}.
* [Common Crawl Foundation's](https://commoncrawl.org/){:target="ccf"} current work on provenance tracking, multilingual data, etc.
* [Coalition for Secure AI](https://www.coalitionforsecureai.org/){:target="csai"} has a work group on software supply chain security concerns. 

The metadata are captured in the dataset card that _every version_ of a dataset carries, including after various stages of processing.

Let's begin.

## Core Requirements

### Ownership

First, to promote fully-traceable provenance and governance, for all data within the dataset, the owner must affirm that they are either (a) the owner of the dataset or (b) you have rights from the owner of the data that enables the dataset to be provided to anyone under the CDLA Permissive 2.0 license. For example, this dataset owner has been granted permission by the source data owners to act on their behalf with respect to enabling others to use it without restriction.

This provision is necessary because many datasets contain data that was obtained by crawling the web, which frequently has mixed provenance and licenses for use.

{: .note}
> **NOTE:** One of the data processing pipelines we are building will carefully filter datasets for such crawled data to ensure our requirements are met for ownership, provenance, license for use, and quality. Until these tools are ready, we are limiting acceptance of crawled datasets.

### Dataset Hosting

Almost all datasets we catalog will remain hosted by the owners, but the AI Alliance can host it for you, when desired.

### A Dataset Card

All useful datasets include _metadata_ about their provenance, license(s), target uses, known limitations and risks, etc. To provide a uniform, standardized way of expressing this metadata, we require every dataset to have a _dataset card_ (or _data card_) that follows the [Hugging Face Dataset Card](https://huggingface.co/docs/hub/datasets-cards){:target="hf-card"} format, where the `README.md` file functions as the dataset card, with our refinements discussed below. This choice reflects the fact that most AI-centric datasets are already likely to be available on the [Hugging Face Hub](https://huggingface.co/){:target="hf"}. 

{: .tip}
> **TIP:** For a general introduction to Hugging Face datasets, see [here](https://huggingface.co/docs/datasets){:target="hf-datasets"}.

#### Quick Steps to Create a Dataset Card

If you need to create a dataset card:

{: .attention}
> 1. Download our version of the Hugging Face dataset card template, <a href="{{site.baseurl}}/files/datasetcard_otdi_template.md.template" download="datasetcard_otdi_template.md"><code>datasetcard_otdi_template.md</code></a>. (If you already have a card in Hugging Face, i.e., the `README.md`, compare our template to your card and add the new fields.)
> 2. Edit the Markdown in the template file to provide the details, as described below.
> 3. [Create the card](https://huggingface.co/docs/datasets/dataset_card){:target="hf-card-create"} in the Hugging Face UI (or edit your existing card.)
> 4. Fill in the metadata fields shown in their editor UI. (See [Table 1](#table-1) below.)
> 5. Paste the rest of your prepared Markdown into the file, after the YAML block delimited by `---`.
> 6. Commit your changes.

## Required Metadata Fields

Refer to the [`datasetcard.md`](https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1){:target="hf-datasetcard-md"} for details about the metadata fields Hugging Face recommends for inclusion in a YAML block at the top of the `README.md`. We comment on these fields below, in [Table 1](#table-1). 

The [`templates/README_guide.md`](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md){:target="hf-guide"} provides additional information about the template fields in their Markdown template file, [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-dataset-card-template"} in the [`huggingface-hub` GitHub repo](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/){:target="hf-hub-repo"}. _However_, we recommend that you use our extended version: <a href="{{site.baseurl}}/files/datasetcard_otdi_template.md.template" download="datasetcard_otdi_template.md"><code>datasetcard_otdi_template.md</code></a>.

### YAML Metadata Block

{: .tip}
> **TIP:** The following tables are long, but starting with the [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-dataset-card-template"} and the [dataset card process](https://huggingface.co/docs/datasets/dataset_card){:target="hf-card-create"} will handle most of the details. Then you can add the additional fields requested in [Table 2](#table-2), those marked with "OTDI".

**Table 1** lists all the fields in the dataset card YAML block. The **R?** (Required?) column uses &#10004; to indicate the field is required by us, &#x274c; for fields that we don't allow (because they are incompatible with this project), and a blank entry indicates a field is optional.

<a name="table-1"></a>

{% include data-spec-table-template.html 
  title="Table 1"
  context=""
  table_id="table1_spec_fields"
  show_source=false
  context=""
%}

<p class="caption"><strong>Table 1:</strong> Hugging Face Datacard Metadata</p>

{: .note}
> **NOTE:** For source code, e.g., the code used for the [data processing pipelines]({{site.baseurl}}/our-processing), the AI Alliance standard code license is [_Apache 2.0_](https://spdx.org/licenses/Apache-2.0){:target="apache"}. For documentation, it is _The Creative Commons License, Version 4.0_, [CC BY 4.0](https://spdx.org/licenses/CC-BY-4.0.html){:target="cc-by-4"}. See the Alliance [`community/CONTRIBUTING` page](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md#licenses){:target="licenses"} for more details about licenses.

## The Markdown Content in the Dataset Card

**Table 2** lists content that we require or recommend in the Markdown body of the dataset card, below the YAML header block. The **Source** column in the table contains the following:
* &ldquo;HF&rdquo; for fields in the Hugging Face [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-dataset-card-template"}. See the [`README_guide.md`](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md){:target="hf-dataset-card-readme"} for descriptions of many of these fields.
<!-- * &ldquo;OTDI&rdquo; for additional fields derived from the [Data Provenance Standard](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"} (OTDI). Where we require OTDI fields, add them to the `README.md` they seem to fit best. -->
* &ldquo;OTDI&rdquo; for additional fields we believe are necessary.

<!-- As noted in the following table, many of the fields appear in both the Hugging Face dataset card template and the Data Provenance Standard, but use different names. We ask you to use the Hugging Face names for consistency and convenience. When unique OTDI fields are used, we convert their field names to lowercase and use underscores as separators, for consistency. -->

<a name="table-2"></a>

{% include data-spec-table-template.html 
  title="Table 2"
  context=""
  table_id="table2_spec_fields"
  show_source=true
  context=""
%}

<p class="caption"><strong>Table 2:</strong> Additional Content for the Dataset Card (<code>README.md</code>)</p>


{% comment %} 
The `Source Metadata for Dataset` field provides lineage from a dataset to its ancestors. It is not necessary to list the entire lineage, just the immediate &ldquo;parents&rdquo;, because the full lineage can be reconstructed from this information. 
{% endcomment %}

For the `personal_and_sensitive_information` field, we recommend using one or more of the following values:

* `Personal Information (PI)/Demographic`
* `Payment Card Industry (PCI)`
* `Personal Financial Information (PFI)`
* `Personally Identifiable Information (PII)`
* `Personal Health Information (PHI)`
* `Sensitive Personal Information (SPI)`
* `Other (please specify)`
* `None`

## Other Considerations for the Data Itself

The [dataset card template]({{site.baseurl}}/dataset-requirements/dataset-card-template) has sections for all the required and optional metadata. This section discusses the data in the dataset.

### Formats

We endeavor to be flexible on dataset file formats and how they are organized. For text, we recommend formats like CSV, JSON, Parquet, ORC, AVRO. Supporting PDFs, where extraction will be necessary, can be difficult, but not impossible.

{: .note}
> **NOTE:** Using Parquet has the benefit that [MLCommons Croissant](https://github.com/mlcommons/croissant){:target="mlc-croissant"} can be used to automatically extract some metadata. See [this Hugging Face page](https://huggingface.co/docs/dataset-viewer/en/croissant){:target="hf-croissant"} and the [`mlcroissant` library](https://huggingface.co/docs/dataset-viewer/en/mlcroissant){:target="mlc-lib"}, which supports loading a dataset using the Croissant metadata. 

### Diverse Datasets

Diverse datasets are desired for creating a variety of AI models and applications with special capabilities.

We are particularly interested in new datasets that can be used to train and tune models to excel in particular domains, or support them through design patterns like RAG and Agents. See [What Kinds of Datasets Do We Want?]({{site.baseurl}}/contributing/#what-kinds-of-datasets-do-we-want) for more information.

Use the `tags` metadata field discussed above to indicate this information, when applicable.

## Derived Dataset Specification

_Every_ dataset that is _derived_ via a processing pipeline from one or more other datasets requires its own dataset card, which must reference all _upstream_ datasets that feed into it (and by extension, their dataset cards of metadata). 

For example, when a derived dataset is the filtered output of one or more _raw_ datasets (defined below), where duplication and offensive content removal was performed, the new dataset may now support different recommended `uses` (i.e., it is now more suitable for model training or more useful for a specific domain), have different `bias_risks_limitations`, and it will need to identify the upstream (ancestor) `source_datasets`.

Suppose a new version of an existing dataset is created, where additional or removed data is involved, but no other changes occur. It also needs a new dataset card, even while most of the metadata will be unchanged.

**Table 3** lists the minimum set of metadata fields that must change in a derived dataset:

<a name="table-3"></a>

{% include data-spec-table-template.html 
  title="Table 3"
  context=""
  table_id="table3_spec_fields"
  show_source=false
  context=""
%}

<p class="caption">Table 3: Minimum Required Dataset Card Changes for a Derived Dataset</p>

### Categories of Dataset Transformations

At this time, we use the following concepts for original and derived datasets, concerning levels of _quality_ and cleanliness. This list corresponds to stages in our _ingestion_ process and subsequent possible derivations of datasets. This list is subject to change.

* **Raw:** A dataset as it is discovered, validated, and cataloged. For all datasets, _our most important concern is **unambiguous provenance** and clear **openness**._ Raw datasets may go through filtering and analysis to remove potential objectionable content.
* **Filtered:** A _raw_ dataset that has gone through a processing pipeline to make it more suitable for specific purposes. This might include removal of duplicate records, filtering for unacceptable content (e.g., hate speech, PII), or filtered for domain-specific content, etc. Since the presence of some content in the raw data could have legal implications for OTDI, such as the presence of some forms of PII and confidential information, we may reject cataloging an otherwise &ldquo;good&rdquo; _raw_ dataset and only catalog a suitable _filtered_ dataset.
* **Structured:** A _filtered_ dataset that has also been reformatted to be most suitable for some AI purpose, such as model training, RAG, etc. For example, PDFs are more convenient to use when converted to JSON or YAML. 
* **Derived:** Any dataset created from one or more other datasets. _Filtered_ and _structured_ datasets are _derived_ datasets.

See [How We Process Datasets]({{site.baseurl}}/our-processing) for more details on these levels and how we process datasets.

After you have prepared or updated the dataset card as required, we will automatically pick up the changes from Hugging Face. If you are not hosting your dataset there, then [contribute your dataset]({{site.baseurl}}/contributing).

