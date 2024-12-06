---
layout: default
title: Dataset Specification
nav_order: 30
has_children: true
---

# Dataset Specification

> **Note:** The specification documented here is the &ldquo;V0.1&rdquo; version of what we think will be required for cataloged datasets. We need and welcome your feedback! Either [contact us]({{site.baseurl}}/about/#contact-us) or consider using [pull requests](https://github.com/The-AI-Alliance/open-trusted-data-initiative/pulls){:target="prs"} with your suggestions. See the AI Alliance community page on [contributing](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md){:target="contrib"} for more details.
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

<!--
The specification is adapted from the following sources:

* [Hugging Face Dataset Card](https://huggingface.co/docs/hub/datasets-cards){:target="hf-card"}
* The [Data Provenance Standard](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"} from the [Data and Trust Alliance](https://dataandtrustalliance.org/){:target="dta"}.
* Unique specification for this project.
-->

The specification is adapted from the [Hugging Face Dataset Card](https://huggingface.co/docs/hub/datasets-cards){:target="hf-card"}, with a few extensions for clearer provenance and governance.

In addition, we are exploring incorporation of the following sources:

* [MLCommons Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} - Consider using Croissant as the primary or perhaps an alternative format for dataset cards. (See also the [Format](#format) section below.)
* BigCode's [dataset card](https://huggingface.co/datasets/bigcode/the-stack#dataset-card-for-the-stack){:target="hf-dataset-card"} for The Stack - What information is there that we should also use.
* [Common Crawl Foundation](https://commoncrawl.org/){:target="ccf"} - work on provenance tracking, multilingual data, etc.
* [Coalition for Secure AI](https://www.coalitionforsecureai.org/){:target="csai"} - e.g., software supply chain is a growing security concern. 
* ...

Most of the details are captured in the dataset card that _every version_ of a dataset carries (e.g., after various stages of processing).

Let's begin.

## The Data Must Be Yours to Contribute

To promote fully-traceable provenance and governance, for all data within the dataset, you must affirm that you are either (a) the owner of the dataset or (b) you have rights from the owner of the data that enables you to provide it to anyone under the CDLA Permissive 2.0 license; for example, you have been granted permission by the owner to act on their behalf with respect to the data and enable others to use it without restriction.

> **WARNING:** Do not contribute any data that was obtained by crawling or scraping public data from the Internet or other public places. At this time, we are not accepting such data because we are seeking to build datasets with a heightened level of clarity around ownership, provenance, and quality.

## Dataset Hosting

You can either retain your current hosting location or you can have the AI Alliance host it for you.

## Dataset Card

All useful datasets include _metadata_ about their provenance, license(s), target uses, known limitations and risks, etc. To provide a uniform, standardized way of expressing this metadata, we ask you to provide a _dataset card_ (or _data card_) when you [contribute the dataset]({{site.baseurl}}/contributing).

Since your dataset is already likely to be available on the [Hugging Face Hub](https://huggingface.co/){:target="hf"}, we ask you create a &ldquo;complete&rdquo; [Hugging Face Dataset Card](https://huggingface.co/docs/hub/datasets-cards){:target="hf-card"} with the metadata fields they support. The project `README.md` file functions as the card. We provide a list below of the fields we consider necessary to be sufficient for our purposes, including a few additional items we need to know that you should add to the `README.md` you create.

> **TIP:** For a general introduction to Hugging Face datasets, see [here](https://huggingface.co/docs/datasets){:target="hf-datasets"}.



## Quick Steps

Here are the steps to create your dataset card, summarized. Read the rest of this page for details:

> 1. Download our version of the Hugging Face dataset card template, <a href="{{site.baseurl}}/files/datasetcard_otdi_template.md.template" download="datasetcard_otdi_template.md"><code>datasetcard_otdi_template.md</code></a>. (If you already have a card in Hugging Face, i.e., the `README.md`, compare our template to your card and add the new fields.)
> 2. Edit the Markdown in the template file to provide the details, as described below.
> 3. [Create the card](https://huggingface.co/docs/datasets/dataset_card){:target="hf-card-create"} in the Hugging Face UI (or edit your existing card.)
> 4. Fill in the metadata fields shown in their editor UI. (See [Table 1](#table-1) below.)
> 5. Paste the rest of your prepared Markdown into the file, after the YAML block delimited by `---`.
> 6. Commit your changes!

### Details

Refer to the [`datasetcard.md`](https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1){:target="hf-datasetcard-md"} for details about the metadata fields Hugging Face (and we!) recommend for inclusion in a YAML block at the top of the `README.md`. We comment on these fields below, see [Table 1](#table-1). 

The [`templates/README_guide.md`](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md){:target="hf-guide"} provides additional information about the template fields in their Markdown template file, [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-dataset-card-template"} in the [`huggingface-hub` GitHub repo](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/){:target="hf-hub-repo"}. _However_, we recommend that you use our extended version: <a href="{{site.baseurl}}/files/datasetcard_otdi_template.md.template" download="datasetcard_otdi_template.md"><code>datasetcard_otdi_template.md</code></a>. (You might need to right click on the link…)

If you want to contribute a dataset that isn't currently hosted in Hugging Face, use the template above to create a dataset card yourself. Manually add the YAML header block, too. Finally, follow the Hugging Face convention of using the `README.md` in the top-level directory as the dataset card.

## Required Metadata

This section describes the minimum set of metadata we expect, including some optional elements of the Hugging Face dataset card that believe are essential.

<!-- This section describes the minimum set of metadata we expect, combining elements of the Hugging Face dataset card, concepts from the [Data Provenance Standard](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"} (DPS) and additional OTDI project specification. -->

All of the fields apply to synthesized data as well as _real_ data, but of course details will be different.

<!-- > **NOTE:** In the tables that follow, many of the fields appear in both the Hugging Face dataset card template and the Data Provenance Standard, but different names are used. We ask you to use the Hugging Face names for consistency and convenience. When unique DPS fields are specified below, we convert their names to lowercase and use underscores as separators, for consistency. -->

### YAML Metadata Block

> **TIP:** The following tables are long, but starting with the [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-dataset-card-template"} and the [dataset card process](https://huggingface.co/docs/datasets/dataset_card){:target="hf-card-create"} will handle most of the details. Then you can add the additional fields requested in [Table 2](#table-2), those marked with "DPS".

Our first table describes the metadata encoded in the YAML header block at the beginning of the Hugging Face README format. See [`datasetcard.md`](https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1){:target="hf-datasetcard"} for details. 

For completeness, the optional fields in that block are also shown. The **Required?** column uses &#9745; to indicate the field is required, empty for optional fields (but often recommended), and &#9746; for fields that we don't allow, because they are incompatible with this project.

<a name="table-1"></a>

| Field Name     | Description     | Required?     | 
| :------------- | :-------------- | :-----------: | 
| `license` | We **strongly recommend** `cdla-permissive-2.0` for the [_Community Data License Agreement – Permissive, Version 2.0_](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md#licenses){:target="cdla"} and may require it in the future [^1]. Use [these names](https://huggingface.co/docs/hub/repositories-licenses){:target="hf-licenses"} for licenses. Also covers the DPS `License to use`. | &#9745; | 
| `license_name` | e.g, _Community Data License Agreement – Permissive, Version 2.0_. | &#9745; | 
| `license_link` | e.g, `LICENSE` or `LICENSE.md` in the same repo or a URL to another location. | &#9745; | 
| `license_details` | Not needed if you use a standard license. |  | 
| `tags` | Useful for indicating target areas for searches, like `chemistry`, `synthetic`, etc. See also `task_categories`. Where applicable, we recommend that you use the categories described below in [Diverse Datasets...](#diverse-datasets). |  | 
| `annotations_creators` | If appropriate. Examples: `crowdsourced`, `found`, `expert-generated`, `machine-generated` (e.g., using _LLMs as judges_). |  | 
| `language_creators` | If appropriate. Examples: `crowdsourced`, `found`, `expert-generated`, `machine-generated` (i.e., synthetic data). |  | 
| `language_details` | One or more of, for example, `en-US`, `fr-FR`, etc. | &#9745; | 
| `pretty_name` | E.g., `Common Chemistry`. This is equivalent to the `Dataset title/name` field in the [Data Provenance Standard](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"} (DPS). | &#9745; | 
| `size_categories` | E.g., `n<1K`, `100K<n<1M`. |  | 
| `source_datasets` | A YAML list; zero or more. Recall our emphasis on _provenance_. This list is very important, as each source must meet our provenance standards. See also the discussions below. | &#9745; | 
| `task_categories` | A YAML list; one or more from the list in [this code](https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/pipelines.ts){:target="hf-tasks"}. | &#9745; | 
| `task_ids` | A YAML list; &ldquo;a unique identifier in the format `lbpp/{idx}`, consistent with HumanEval and MBPP&rdquo; from [here](https://huggingface.co/datasets/CohereForAI/lbpp){:target="cohere"}. See also examples [here](https://huggingface.co/datasets/CohereForAI/lbpp){:target="humaneval"}. |  | 
| `paperswithcode_id` | Dataset id on PapersWithCode (from the URL). |  | 
| `configs` | Can be used to pass additional parameters to the dataset loader, such as `data_files`, `data_dir`, and any builder-specific parameters. |  | 
| `config_name` | One or more dataset subsets, if applicable. See the example in [`datasetcard.md`](https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1){:target="hf-datasetcard"} and the discussions [here](https://huggingface.co/docs/hub/en/datasets-manual-configuration){:target="hf-manual"} and [here](https://huggingface.co/docs/datasets/main/en/repository_structure){:target="hf-structure"}. |  | 
| `dataset_info` | Can be used to store the feature types and sizes of the dataset to be used in Python. See the discussion in [`datasetcard.md`](https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1){:target="hf-datasetcard"}. Also covers the DPS `Data format` field. |  | 
| `extra_gated_fields` | Used for protected datasets and hence incompatible with the goals of OTDI. | &#9746; | 
| `train-eval-index` | Add this if you want to encode a train and evaluation info in a structured way for AutoTrain or Evaluation on the Hub. See the discussion in [`datasetcard.md`](https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1){:target="hf-datasetcard"}. |  | 
{: .metadata-table}
<p class="caption">Table 1: Hugging Face Datacard Metadata</p>

[^1]: For source code, e.g., the code used for the [data processing pipelines]({{site.baseurl}}/our-processing), the AI Alliance standard code license is [_Apache 2.0_](https://spdx.org/licenses/Apache-2.0){:target="apache"}. For documentation, it is _The Creative Commons License, Version 4.0_, [CC BY 4.0](https://spdx.org/licenses/CC-BY-4.0.html){:target="cc-by-4"}. See the Alliance [`community/CONTRIBUTING` page](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md#licenses){:target="licenses"} for more details about licenses.

## The Markdown Content in the Dataset Card

Our second table lists content that we require or recommend in the Markdown body of the dataset card, below the YAML header block. The **Source** column in the table contains the following:
* &ldquo;HF&rdquo; for fields in the Hugging Face [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-dataset-card-template"}. See the [`README_guide.md`](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md){:target="hf-dataset-card-readme"} for descriptions of many of these fields.
* &ldquo;DPS&rdquo; for additional fields derived from the [Data Provenance Standard](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"} (DPS). Where we require DPS fields, add them to the `README.md` they seem to fit best.
* &ldquo;OTDI&rdquo; for project-specific specification. 

As noted in the following table, many of the fields appear in both the Hugging Face dataset card template and the Data Provenance Standard, but use different names. We ask you to use the Hugging Face names for consistency and convenience. When unique DPS fields are used, we convert their field names to lowercase and use underscores as separators, for consistency.

<a name="table-2"></a>

| Field Name     | Description     | Required?     | Source     |
| :------------- | :-------------- | :-----------: | :--------: |
| `standards_version_used` | (DPS name: `Standards version used`) The DPS schema version. Since our dataset card specification are not strictly conformant to any DPS schema, this is optional. |  | DPS | 
| `unique_metadata_identifier` | (DPS name: `Unique Metadata Identifier`) A UUID (DPS allows other choices) that is globally unique. Derived datasets must have their own UUIDs. The UUID is very useful for unambiguous lineage tracking, which is why we require it. | &#9745; | DPS, OTDI |
| `metadata_location` | (DPS name: `Metadata Location`) Where the metadata is located. However, by definition, we require the `README.md` file, so omit this field. | &#9746; | DPS |
| `dataset_summary` | A concise summary of the dataset and its purpose. | &#9745; | HF | 
| `dataset_description` | (DPS name: `Description of the Dataset`) Describe the contents, scope, and purpose of the dataset, which helps users understand what the data represents, how it was collected, and any limitations or recommended uses. However, this field should not include redundant information covered elsewhere. | &#9745; | HF, DPS | 
| `curated_by` | One or more legal entities responsible for creating the dataset, providing accountability and a point of contact for inquiries. Called `Dataset issuer` in DPS. See also `dataset_card_authors` below. | &#9745; | HF, DPS |
| `dataset_sources` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#dataset-sources-optional){:target="hf-datasetcard-template-sources"} (from [`datasetcard_template.md`](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md){:target="hf-datasetcard-template"}). Complements the information provided above for `source_datasets`. The `Repository` URL &ldquo;subfield&rdquo; is required for each source dataset, _unless_ it was provided by `source_datasets` in [Table 1](#table-1). The `Paper` and `Demo` subfields are optional. See also `source_data` and `source_metadata_for_dataset` next. | &#9745; | HF |
| `source_data` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#source-data){:target="hf-datasetcard-template-source-data"}. Use the subsections, described next, `data_collection_and_processing_section` and `source_data_producers_section` to describe important provenance information. Is the data synthetic or not? This section also covers the DPS `Method` and `Source (if different from issuer)` fields. The latter is more explicit about when data comes from third-party sources. Note our specification above that you can only submit datasets where you have the necessary rights (see also `consent_documentation_location` below). | &#9745; | HF, DPS |
| `data_collection_and_processing_section` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#source-data){:target="hf-datasetcard-template-source-data"}. Describes the data collection and processing process such as data selection criteria, filtering and normalization methods, tools and libraries used, etc. | &#9745; | HF |
| `source_data_producers_section` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#source-data){:target="hf-datasetcard-template-source-data"}. This section describes the people or systems who originally created the data. It should also include self-reported demographic or identity information for the source data creators if this information is available. | &#9745; | HF |
| `source_metadata_for_dataset` | (DPS name: `Source metadata for dataset`) Additional content for `source_data`; if the corresponding metadata for any dataset is not part of that dataset, then it must be explicitly linked here. This information is necessary for lineage tracking, part of our provenance objectives. Marked required, but if all metadata is part of all datasets (e.g., in `README.md` dataset cards), then this field can be omitted. | &#9745; | DPS |
| `consent_documentation_location` | (DPS name: `Consent documentation location`) &ldquo;Specifies where consent documentation or agreements related to the data can be found, which help enable legal compliance and regulatory use.&rdquo; Required for third-party datasets you are contributing. | &#9745; | DPS |
| `data_origin_geography` | (DPS name: `Data origin geography`) &ldquo;The geographical location where the data was originally collected, which can be important for compliance with regional laws and understanding the data's context.&rdquo; Required if restrictions apply. |  | DPS |
| `data_processing_geography_inclusion_exclusion` | (DPS name: `Data Processing Geography Inclusion/Exclusion`) &ldquo;Defines the geographical boundaries within which the data can or cannot be processed, often for legal or regulatory reasons.&rdquo; Required if restrictions apply. |  | DPS |
| `data_storage_geography_inclusion_exclusion` | (DPS name: `Data Storage Geography Inclusion/Exclusion`) &ldquo;Specifies where the data is stored and any geographical restrictions on storage locations, crucial for compliance with data sovereignty laws.&rdquo; Required if restrictions apply. |  | DPS |
| `uses` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#uses){:target="hf-datasetcard-template-uses"}. Optional, but useful for describing `Direct Use` (field name: `direct_use`) and `Out-of-Scope Use` (field name: `out_of_scope_use`) for the dataset. Consider structuring the `Direct Use` as described in the `Supported Tasks and Leaderboards` [section](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md#supported-tasks-and-leaderboards){:target="hf-dataset-card-readme-guide"} in the `templates/README_guide.md`. |  | HF |
| `annotations` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#annotations){:target="hf-datasetcard-template-annotations"}. Add any additional information for the `annotations_creators` above, if any. Subsections are `annotation_process_section` and `who_are_annotators_section`. |  | HF |
| `annotation_process_section` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#annotations){:target="hf-datasetcard-template-annotations"}. Describes the annotation process such as annotation tools used in the process, the amount of data annotated, annotation guidelines provided to the annotators, inter-annotator statistics, annotation validation, etc. |  | HF |
| `who_are_annotators_section` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#annotations){:target="hf-datasetcard-template-annotations"}. Describes the people or systems who created the annotations. |  | HF |
| `bias_risks_limitations` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#bias-risks-and-limitations){:target="hf-datasetcard-template-bias-risks-and-limitations"}. While provenance and governance are the top priorities for OTDI, we also want to communicate to potential users what risks they need to understand about our cataloged datasets. Therefore, we require any information you can provide in this section, along with the `Recommendations` subsection for mitigations, if known. | &#9745; | HF |
| `personal_and_sensitive_information` | (DPS name: `Confidentiality classification`), State whether the dataset contains data that might be considered personal, sensitive, or private (e.g., data that reveals addresses, uniquely identifiable names or aliases, racial or ethnic origins, sexual orientations, religious beliefs, political opinions, financial or health data, etc.). Consider using one or more  of the values listed below, after this table. If efforts were made to anonymize the data, describe the anonymization process and also fill in `use_of_privacy_enhancing_technologies_pets`. | &#9745; | HF, DPS |
| `use_of_privacy_enhancing_technologies_pets` | (DPS name: `Use of Privacy Enhancing Technologies (PETs)...`), &ldquo;Indicates whether techniques were used to protect personally identifiable information (PII) or sensitive personal information (SPI), highlighting the dataset's privacy considerations.&rdquo; | &#9745; | DPS |
| `citation` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#citation){:target="hf-datasetcard-template-citation"}. A place to add `BibTeX` (field name: `citation_bibtex`) and `APA` (field name: `citation_apa`) citations. |  | HF |
| `glossary` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#glossary){:target="hf-datasetcard-template-glossary"}. Define useful terms. |  | HF |
| `dataset_card_authors` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#dataset-card-authors-optional){:target="hf-datasetcard-template-dataset-card-authors"}. We need to know the authors. | &#9745; | HF |
| `dataset_card_contact` | [HF template section](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#dataset-card-contact){:target="hf-datasetcard-template-dataset-card-contact"}. We need to know whom to contact when needed. Okay to leave blank if the authors' contact information is provided. | | HF |
| `dataset_issue_date` | (DPS name: `Dataset Issue Date`) When the dataset was compiled or created. (New versions require new dataset cards.) Recommended format: `YYYY-mm-dd:THH:MM:SS` | &#9745; | DPS |
| `date_previously_issued_version_dataset` | (DPS name: `Date of Previously Issued Version of the Dataset`) Timestamp for previous releases, if applicable. Redundant with other traceability tools, so not recommended. |  | DPS |
| `range_dates_data_generation` | (DPS name: `Range of dates for data generation`) The span of time during which the data within the dataset was collected or generated, offering insight into the dataset's timeliness and relevance. | &#9745; | DPS |
| `intended_data_use` | (DPS name: `Intended Data Use`) Covered by other fields, so omit. | &#9746; | DPS |
| `proprietary_data_presence` | (DPS name: `Proprietary Data Presence`) Incompatable with OTDI goals, so either omit or always use `no`. | &#9746; | DPS |
{: .metadata-table}
<p class="caption">Table 2: Additional Content for the Dataset Card (`README.md`)</p>

The `Source Metadata for Dataset` field provides lineage from a dataset to its ancestors. It is not necessary to list the entire lineage, just the immediate &ldquo;parents&rdquo;, because the full lineage can be reconstructed from this information.

For the `personal_and_sensitive_information` (DPS' `Confidentiality Classification`) field, consider using one or more of the following values defined by DPS:

* `Personal Information (PI)/Demographic`
* `Payment Card Industry (PCI)`
* `Personal Financial Information (PFI)`
* `Personally Identifiable Information (PII)`
* `Personal Health Information (PHI)`
* `Sensitive Personal Information (SPI)`
* `Other (please specify)`
* `None`

## Some Specification for the Data Itself

The [dataset card template]({{site.baseurl}}/dataset-specification/dataset-card-template) has sections for all the required and optional information. Here we discuss a few points.

### Formats

We endeavor to be flexible on dataset file formats and how they are organized. For text, we recommend formats like CSV, JSON, Parquet, ORC, AVRO. Supporting PDFs, where extraction will be necessary, can be difficult, but not impossible.

> **NOTE:** Using Parquet has the benefit that [MLCommons Croissant](https://github.com/mlcommons/croissant){:target="mlc-croissant"} can be used to automatically extract some metadata. See [this Hugging Face page](https://huggingface.co/docs/dataset-viewer/en/croissant){:target="hf-croissant"} and the [`mlcroissant` library](https://huggingface.co/docs/dataset-viewer/en/mlcroissant){:target="mlc-lib"}, which supports loading a dataset using the Croissant metadata. 

<a name="diverse-datasets"></a>
### Diverse Datasets Desired for Diverse AI Models and Applications

We are particularly interested in new datasets that can be used to train and tune models to excel in various domains, although general-purpose datasets are also welcome, of course. 

These are the current domains of particular interest. Use the `tags` metadata field discussed above to indicate domains, when applicable.

#### Science and Industrial

* `Climate`: Supporting research in climate change, modeling vegetation and water cover, studying agriculture, etc.
* `Marine`: Supporting research on and applications targeted towards marine environments.
* `Materials`: Known chemical and mechanical properties of chemicals useful for research into potential new and existing materials. 
* `Semiconductors`: Specific area of materials research focused on improving the state of the art for semiconductor performance and manufacturing.

Other science and industrial domains are welcome, too. 

#### Other Domains

* `Finance`: Historical market activity and behaviors. Connections to influences like climate, weather events, political events, etc. 
* `Healthcare`: Everything from synthetic patient data for modeling outcomes, to public literature on known diseases and conditions, to diagnostics results and their analysis.
* `Legal`: Jurisdiction-specific data about case law, etc.
specific applications.
* `Social Sciences`: Social dynamics, political activity and sentiments, etc.
* `Timeseries`: Data for training, tuning, and testing time series models, including specific applications.

#### Modalities

In addition, we welcome datasets with different _modalities_. Hugging Face attempts to determine the modalities of datasets, but you can also use the `tags` to indicate modalities, such as the following:

* `Text`:
* `Image`: i.e., still images
* `Audio`: 
* `Video`: including optional audio

## Derived Dataset Specification

_Every_ dataset that is derived via a processing pipeline from one or more other datasets requires its own dataset card, which must reference all _upstream_ datasets that feed into it (and by extension, their dataset cards of metadata). Similarly, each new version of an existing dataset, whre only additional (or removed) data is involved, also needs an updated card, but more of the metadata will be unchanged.

> **Note:** We are considering a way to allow a derived dataset card to just specify what's new or changed and inherit unchanged metadata from its ancestors. Also, when automated pipelines are used to create derived datasets, our [processing pipelines]({{site.baseurl}}/our-processing) will automatically generate some updated metadata, such as timestamps, processing tools and steps, etc.

When the derived dataset is the filtered output of one or more _raw_ datasets (defined below), where duplication and offensive content removal was performed, the new dataset may support different `uses`, have different `bias_risks_limitations`, and it will need to identify the upstream (ancestor) `source_datasets`, for example.

Table 3 lists the fields that must change (with some exceptions), to avoid ambiguities:

<a name="table-3"></a>

| Field Name     | Possible Updates     | Required?     |
| :------------- | :------------------- | :-----------: |
| `pretty_name` | A modified name is strongly recommended to avoid potential confusion. It might just embed a version string. | |
| `unique_metadata_identifer` | Must be new! | &#9745; |
| `dataset_issue_date`   | The date for this new card. | &#9745; |

{: .metadata-table}
<p class="caption">Table 4: Required Dataset Card Changes for a Derived Dataset</p>

### Categories of Dataset Transformations

At this time, we have the following concepts for original and derived datasets, concerning levels of _quality_ and cleanliness. This list corresponds to stages in our _ingestion_ process and subsequent possible derivations of datasets. This list is subject to change.

* **Raw:** The dataset as submitted, which could already be in &ldquo;good shape&rdquo;. _Our most important concern at this stage is **unambiguous provenance**._ Raw datasets may go through filtering and analysis to remove potential objectionable content. However, the presence of some content in the raw data could have legal implications, such as some forms of PII and company confidential information, which may force us to reject the contribution. (Should this happen, we will discuss mitigation options with you.)
* **Filtered:** A _raw_ dataset that has gone through a processing pipeline to remove duplicates, filter for objectional content, etc.
* **Structured:** A _filtered_ dataset that has been reformatted to be most suitable for model training (LLMs, time series, etc.), RAG patterns, and similar purposes. For example, PDFs converted to JSON. 

See [How We Process Datasets]({{site.baseurl}}/our-processing) for more details on these levels and how we process datasets.

After you have prepared or updated the dataset card as required, it's time to [contribute your dataset]({{site.baseurl}}/contributing)!

