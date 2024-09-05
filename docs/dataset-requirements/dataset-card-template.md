---
layout: default
title: Dataset Card Template
nav_order: 200
parent: Dataset Requirements
has_children: false
---

Use the following template to create your dataset card. Replace all the content marked with `{...}` with appropriate values and add additional text as you see fit. Note the HTML-style comments `<!-- ... -->`, which you can remove, and also pay attention to sections marked required. Keep in mind our goals for OTDI and how this metadata supports those goals.  

If you are uncertain about what a particular section requires, add questions in that section! When you submit this card with your dataset, we will provide answers, as well as other feedback. 

For more information on dataset card metadata, see the [Hugging Face guide](https://huggingface.co/docs/hub/datasets-cards) and their [card specification](https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1), from which this card template is adapted.

> **NOTE:** We intend to turn this template into a form for easier preparation. Apologies in the meantime...

Here is the template:

# Dataset Card for { descriptive, unique name }

## Short Description (Required)

<!-- Provide a quick summary of the dataset and its purpose. -->

{ dataset_summary }

## Dataset Details 

### Dataset Description (Required)

<!-- Provide longer details about this dataset, it's purpose, goals, etc. Note that some of the bullet list items are expanded below, so use the bullets when a single, concise entry is known, or use the longer sections below. -->

{ dataset_description }

* **Curated by (required):** { curators_list } (Required)
* **Funded by (optional):** { funded_by }
* **Shared by (optional):** { shared_by, e.g., your name and email } <!-- The submission form will also have this. -->
* **Language(s) (NLP):** { language_list } <!-- include the primary languages you know of -->


### Dataset Card Authors (Required)

{ dataset_card_authors }

### Dataset Card Contacts {Required}

<!-- Email addresses for one or more of authors or other contact people -->

{ dataset_card_contacts }

### Dataset Sources

<!-- Provide the basic links for the dataset. While this information will also be in the submission form, we want to have it in the data card, as well. -->

- **Repository (required):** { repo_URL } <!-- e.g., https://huggingface.co/datasets/... -->
- **Paper (optional):** { paper_URL } <!-- e.g., arxiv.org link -->
- **GitHub (optional):** { GitHub_URL } <!-- e.g., for supporting code and documentation -->
- **Other Demo or Documentation Links (optional):** { URL_list }

### Notes on How to Use the Dataset

<!-- Address questions around how the dataset is intended to be used. For example, is it only suitable for use certain models, modalities, tools? -->

{ how_to_use_the_dataset }

### Target Use Cases

<!-- Describes suitable use cases for the dataset. -->

{ target_use_cases }

### Out-of-Scope Use Cases

<!-- This section addresses misuse, malicious use, and uses that the dataset will not work well for. -->

{ out_of_scope_use_cases }

### Dataset Structure

<!-- This section provides a description of the dataset format, directory structure, fields, and additional information about the dataset structure such as criteria used to create the splits, relationships between data points, etc. -->

{ dataset_structure }

### Dataset Creation

#### Curation Rationale

<!-- Motivation for the creation of this dataset. -->

{ curation_rationale_section }

#### Source Data (Required)

<!-- This section describes the source data (e.g. news text and headlines, social media posts, translated sentences, ...) used to create your dataset. Because of our emphasis on provenance, you must provide explicit details about any sources you used, including information about provenance, license to use, etc. -->

{ source_data }

#### Data Collection and Processing (Required)

<!-- This section describes the data collection and processing process such as data selection criteria, filtering and normalization methods, tools and libraries used, etc. While we understand you may not want to reveal any proprietary methods used, please provide enough information to satisfy our provenance concerns. -->

{ data_collection_and_processing }

#### Source Data Producers (Required)

<!-- This section describes the people or systems who originally created the data. It should also include self-reported demographic or identity information for the source data creators if this information is available. Provide enough information to satisfy our provenance concerns. -->

{ source_data_producers }

### Annotations (Optional)

<!-- If the dataset contains annotations which are not part of the initial data collection, use this section to describe them. -->

{ annotations }

#### Annotation Process

<!-- This section describes the annotation process such as annotation tools used in the process, the amount of data annotated, annotation guidelines provided to the annotators, interannotator statistics, annotation validation, etc. -->

{ annotation_process }

#### Who Are the Annotators?

<!-- This section describes the people or systems who created the annotations. -->

{ who_are_annotators }

### Personal and Sensitive Information (Required)

<!-- State whether the dataset contains data that might be considered personal, sensitive, or private (e.g., data that reveals addresses, uniquely identifiable names or aliases, racial or ethnic origins, sexual orientations, religious beliefs, political opinions, financial or health data, etc.). If efforts were made to anonymize the data, describe the anonymization process. -->

{ personal_and_sensitive_information }

### Bias, Risks, and Limitations (Required)

<!-- This section describes any known technical and social limitations of the dataset. -->

{ bias_risks_limitations }

#### Recommendations

<!-- This section is meant to convey any additional recommendations with respect to known bias, risk, and technical limitations. Note that we will always warn users "to be aware of potential risks, biases, and limitations of this dataset, which may not be fully known." -->

{ bias_recommendations }

### Licensing Information

The dataset is released under the **Community Data License Agreement – Permissive, Version 2.0** [license](https://cdla.dev/permissive-2-0/).

### Future Work

<!-- Describe planned work, if any. -->

{ future_work }

### Citation (Optional)

<!-- If there is a paper or blog post introducing the dataset, the APA and Bibtex information for that should go in this section. If they don't exist, delete these entries. -->

**BibTeX:**

{ citation_bibtex }

**APA:**

{ citation_apa }

## Glossary (Optional)

<!-- If relevant, include terms and calculations in this section that can help readers understand the dataset or dataset card. If there are none, just use "N/A". -->

{ glossary }

## More Information (Optional)

<!-- Anything else you want to add? -->

{ more_information }

