---
layout: default
title: Dataset Specification
nav_order: 30
has_children: false
---

# Dataset Specification

{: .note}
> **Note:** The specification documented here is the &ldquo;V0.1.7&rdquo; version of the criteria we believe are required for datasets cataloged by OTDI. We need and welcome your feedback! Either [contact us]({{site.baseurl}}/about/#contact-us) or consider using [pull requests](https://github.com/The-AI-Alliance/open-trusted-data-initiative/pulls){:target="prs"} with your suggestions. See the AI Alliance community page on [contributing](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md){:target="contrib"} for more details.
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

**Table 1** lists all the fields in the dataset card YAML block. The **Required or Disallowed?** column uses &#10004; to indicate the field is required by us, &#x274c; for fields that we don't allow (because they are incompatible with this project), and a blank entry indicates a field is optional.

<a name="table-1"></a>

{% include specification-table-template.html 
  title="YAML Metadata Block"
  context=""
  table_id="yaml_metadata_block_spec_fields"
  show_source=false
  context=""
%}

<p class="caption"><strong>Table 1:</strong> Hugging Face Datacard YAML Metadata Block</p>

{: .note}
> **NOTE:** For source code, e.g., the code used for the [data processing pipelines]({{site.baseurl}}/our-processing), the AI Alliance standard code license is [_Apache 2.0_](https://spdx.org/licenses/Apache-2.0){:target="apache"}. For documentation, it is _The Creative Commons License, Version 4.0_, [CC BY 4.0](https://spdx.org/licenses/CC-BY-4.0.html){:target="cc-by-4"}. See the Alliance [`community/CONTRIBUTING` page](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md#licenses){:target="licenses"} for more details about licenses.


## The Markdown Content in the Dataset Card

**Table 2** lists content that we require or recommend in the Markdown body of the dataset card, below the YAML header block. The **Source** column in the table contains the following:
* &ldquo;HF&rdquo; for fields in the Hugging Face [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-dataset-card-template"}. See the [`README_guide.md`](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md){:target="hf-dataset-card-readme"} for descriptions of many of these fields.
<!-- * &ldquo;OTDI&rdquo; for additional fields derived from the [Data Provenance Standard](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"} (OTDI). Where we require OTDI fields, add them to the `README.md` they seem to fit best. -->
* &ldquo;OTDI&rdquo; for additional fields we believe are necessary.

<!-- As noted in the following table, many of the fields appear in both the Hugging Face dataset card template and the Data Provenance Standard, but use different names. We ask you to use the Hugging Face names for consistency and convenience. When unique OTDI fields are used, we convert their field names to lowercase and use underscores as separators, for consistency. -->

<a name="table-2"></a>

{% include specification-table-template.html 
  title="Markdown Metadata Content"
  context=""
  table_id="markdown_metadata_content_spec_fields"
  show_source=true
  context=""
%}

<p class="caption"><strong>Table 2:</strong> Additional Markdown Metadata Content in the Dataset Card (<code>README.md</code>)</p>


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

<a id="derived-dataset-specification"></a>

## Derived or Synthetic Dataset Specification

_Every_ dataset that is _derived_ or _synthesized_ via a processing pipeline from one or more other datasets or models requires its own dataset card, which must reference all _upstream_ datasets and models that feed into it (and by extension, their dataset and model cards of metadata). 

For example, when a derived dataset is the filtered output of one or more _raw_ (defined below) datasets, where duplication and offensive content removal was performed, the new dataset may now support different recommended `uses` (i.e., it is now more suitable for model training or more useful for a specific domain), have different `bias_risks_limitations`, and it will need to identify the upstream (ancestor) `source_datasets`.

Suppose a new version of an existing dataset is created, where additional or removed data is involved, but no other changes occur. It also needs a new dataset card, even while most of the metadata will be unchanged.

Finally, what if several datasets are used to derive a new dataset and these upstream data sources have different licenses? What if synthetic data is generated using a model? **_The &ldquo;most restrictive&rdquo; upstream license must be used or a suitable alternative._** For example, if one upstream source is not permissively licensed, the data from it in the derived dataset can't be &ldquo;made&rdquo; permissive by using a more permissive license. The whole derived dataset **must** use the most restrictive license attached to the upstream datasets. Similarly, a synthetic dataset generated from a model has to be licensed in accordance with the terms of use for the model. Some commercial models don't allow generated content to be used in permissively-licensed datasets, for example.

{: .note}
> **NOTE:** The derived dataset license must match the &ldquo;most restrictive&rdquo; upstream license or a similarly-restrictive alternative must be used. For synthetic data generated by a model, the terms of service for the model must be supported by the new dataset's license.

**Table 3** lists the minimum set of metadata fields that must change in a derived dataset:

<a name="table-3"></a>

{% include specification-table-template.html 
  title="Derived Dataset Requirements"
  context=""
  table_id="derived_dataset_requirements_spec_fields"
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

## Appendix: Task Categories

The `task_categories` field in [**Table 1**](#table-1) above recommends using the &ldquo;types&rdquo; in [this list](https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/pipelines.ts){:target="hf-tasks"} in Hugging Face source code. For convenience, here is the same list, as of November 2025:

Here we group the task types by _modality_ (e.g., `nlp`). Some tasks have defined subtask types, which are listed with them. If no subtasks are shown, none are defined for the task type.

### Natural Language Processing - `nlp`

| **Task Type** | **Subtask Type** | **Name** |
| :------------ | :--------------- | :------- |
| `text-classification` |                    | Text Classification |
| | `acceptability-classification`           | Acceptability Classification |
| | `entity-linking-classification`          | Entity Linking Classification |
| | `fact-checking`                          | Fact Checking |
| | `intent-classification`                  | Intent Classification |
| | `language-identification`                | Language Identification |
| | `multi-class-classification`             | Multi Class Classification |
| | `multi-label-classification`             | Multi Label Classification |
| | `multi-input-text-classification`        | Multi-input Text Classification |
| | `natural-language-inference`             | Natural Language Inference |
| | `semantic-similarity-classification`     | Semantic Similarity Classification |
| | `sentiment-classification`               | Sentiment Classification |
| | `topic-classification`                   | Topic Classification |
| | `semantic-similarity-scoring`            | Semantic Similarity Scoring |
| | `sentiment-scoring`                      | Sentiment Scoring |
| | `sentiment-analysis`                     | Sentiment Analysis |
| | `hate-speech-detection`                  | Hate Speech Detection |
| | `text-scoring`                           | Text Scoring |
| `token-classification` |                   | Token Classification | 
| | `named-entity-recognition`               | Named Entity Recognition |
| | `part-of-speech`                         | Part of Speech |
| | `parsing`                                | Parsing |
| | `lemmatization`                          | Lemmatization |
| | `word-sense-disambiguation`              | Word Sense Disambiguation |
| | `coreference-resolution`                 | Coreference-resolution |
| `table-question-answering` |               | Table Question Answering |
| `question-answering` |                     | Question Answering | 
| | `extractive-qa`                          | Extractive QA | 
| | `open-domain-qa`                         | Open Domain QA | 
| | `closed-domain-qa`                       | Closed Domain QA | 
| `zero-shot-classification` |               | Zero-Shot Classification | 
| `translation` |                            | Translation |
| `summarization` |                          | Summarization | 
| | `news-articles-summarization`            | News Articles Summarization |
| | `news-articles-headline-generation`      | News Articles Headline Generation |
| `feature-extraction` |                     | Feature Extraction |
| `text-generation` |                        | Text Generation |
| | `dialogue-modeling`                      | Dialogue Modeling |
| | `dialogue-generation`                    | Dialogue Generation |
| | `conversational`                         | Conversational |
| | `language-modeling`                      | Language Modeling |
| | `text-simplification`                    | Text Simplification |
| | `explanation-generation`                 | Explanation Generation |
| | `abstractive-qa`                         | Abstractive QA |
| | `open-domain-abstractive-qa`             | Open Domain Abstractive QA |
| | `closed-domain-qa`                       | Closed Domain QA |
| | `open-book-qa`                           | Open Book QA |
| | `closed-book-qa`                         | Closed Book QA |
| | `text2text-generation`                   | Text2Text Generation |
| `fill-mask` |                              | Fill Mask |
| | `slot-filling`                           | Slot Filling |
| | `masked-language-modeling`               | Masked Language Modeling |
| `table-to-text` |                          | Table to Text |
| `multiple-choice` |                        | Multiple Choice |
| | `multiple-choice-qa`                     | Multiple Choice QA |
| | `multiple-choice-coreference-resolution` | Multiple Choice Coreference Resolution |
| `text-ranking`   |                         | Text Ranking |
| `text-retrieval` |                         | Text Retrieval |
| | `document-retrieval`                     | Document Retrieval |
| | `utterance-retrieval`                    | Utterance Retrieval |
| | `entity-linking-retrieval`               | Entity Linking Retrieval |
| | `fact-checking-retrieval`                | Fact Checking Retrieval  |

### Audio - `audio`

| **Task Type** | **Subtask Type** | **Name** |
| :------------ | :--------------- | :------- |
| `sentence-similarity` |           | Sentence Similarity |
| `text-to-speech` |                | Text-to-Speech |
| `text-to-audio` |                 | Text-to-Audio |
| `automatic-speech-recognition` |  | Automatic Speech Recognition |
| `audio-to-audio` |                | Audio-to-Audio |
| `audio-classification` |          | Audio Classification |
| | `keyword-spotting`              | Keyword Spotting |
| | `speaker-identification`        | Speaker Identification |
| | `audio-intent-classification`   | Audio Intent Classification |
| | `audio-emotion-recognition`     | Audio Emotion Recognition |
| | `audio-language-identification` | Audio Language Identification |
| `voice-activity-detection` |      | Voice Activity Detection | 

### Multimodal - `multimodal`

For `visual-question-answering` and `document-question-answering`, the Hugging Face source file lists each as its own subtask, which looks like a data error, but we show it for consistency.

| **Task Type** | **Subtask Type** | **Name** |
| :------------ | :--------------- | :------- |
| `audio-text-to-text` |          | Audio-Text-to-Text |
| `image-text-to-text` |          | Image-Text-to-Text |
| `visual-question-answering` |   | Visual Question Answering |
| | `visual-question-answering`   | Visual Question Answering |
| `document-question-answering` | | Document Question Answering |
| | `document-question-answering` | Document Question Answering |
| `video-text-to-text` |          | Video-Text-to-Text |
| `visual-document-retrieval` |   | Visual Document Retrieval |
| `any-to-any` |                  | Any-to-Any |


### Computer Vision - `cv`

| **Task Type** | **Subtask Type** | **Name** |
| :------------ | :--------------- | :------- |
| `depth-estimation` |                 | Depth Estimation |
| `image-classification` |             | Image Classification |
| | `multi-label-image-classification` | Multi Label Image Classification |
| | `multi-class-image-classification` | Multi Class Image Classification |
| `object-detection` |                 | Object Detection |
| | `face-detection`                   | Face Detection    |
| | `vehicle-detection`                | Vehicle Detection |
| `image-segmentation` |               | Image Segmentation |
| | `instance-segmentation`            | Instance Segmentation |
| | `semantic-segmentation`            | Semantic Segmentation |
| | `panoptic-segmentation`            | Panoptic Segmentation |
| `text-to-image` |                    | Text-to-Image |
| `image-to-text` |                    | Image-to-Text |
| | `image-captioning`                 | Image Captioning |
| `image-to-image` |                   | Image-to-Image |
| | `image-inpainting`                 | Image Inpainting   |
| | `image-colorization`               | Image Colorization |
| | `super-resolution`                 | Super Resolution     |
| `image-to-video` |                   | Image-to-Video |
| `unconditional-image-generation` |   | Unconditional Image Generation |
| `video-classification` |             | Video Classification |
| `text-to-video` |                    | Text-to-Video |
| `zero-shot-image-classification` |   | Zero-Shot Image Classification |
| `mask-generation` |                  | Mask Generation |
| `zero-shot-object-detection` |       | Zero-Shot Object Detection |
| `text-to-3d`  |                      | Text-to-3D  |
| `image-to-3d` |                      | Image-to-3D |
| `image-feature-extraction` |         | Image Feature Extraction |
| `keypoint-detection` |               | Keypoint Detection |
| `pose-estimation` |                  | Pose Estimation |
| `video-to-video` |                   | Video-to-Video |


### Reinforcement Learning - `rl`

| **Task Type** | **Subtask Type** | **Name** |
| :------------ | :--------------- | :------- |
| `reinforcement-learning` | | Reinforcement Learning |
| `robotics` |               | Robotics |
| | `grasping`               | Grasping      |
| | `task-planning`          | Task Planning |

### Tabular - `tabular`

| **Task Type** | **Subtask Type** | **Name** |
| :------------ | :--------------- | :------- |
| `tabular-classification` |               | Tabular Classification |
| | `tabular-multi-class-classification`   | Tabular Multi Class Classification |
| | `tabular-multi-label-classification`   | Tabular Multi Label Classification |
| `tabular-regression` |                   | Tabular Regression |
| | `tabular-single-column-regression`     | Tabular Single Column Regression |
| `tabular-to-text` |                      | Tabular to Text |
| | `rdf-to-text`                          | RDF to text |
| `time-series-forecasting` |              | Time Series Forecasting |
| | `univariate-time-series-forecasting`   | Univariate Time Series Forecasting   |
| | `multivariate-time-series-forecasting` | Multivariate Time Series Forecasting |

### Other - `other`

Special cases that don't fit in the other modality categories.

| **Task Type** | **Subtask Type** | **Name** |
| :------------ | :--------------- | :------- |
| `graph-ml` | | Graph Machine Learning |
| `other`    | | Other |
